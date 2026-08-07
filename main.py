import os
import time
import schedule # Importar la librería schedule
from datetime import datetime
from collections import defaultdict # Para el caché y agrupación
from dotenv import load_dotenv
from helpers.handlers.printer import log
from helpers.constants.definitions import olt_devices, endpoints
from helpers.handlers.request import db_request, odoo_request
from scripts.CA import CA,sending_mail
from helpers.handlers.mail_sender import send_mail, send_no_clients_mail


global last_resp
global last_scan_time
global odoo_clients_cache
global cajera_totals_cache
global last_cache_update_time

last_resp = []
last_scan_time = None
odoo_clients_cache = {}
cajera_totals_cache = defaultdict(int)
last_cajeras_alertas = {}

load_dotenv()

# Definir la función que contiene la lógica principal y el envío de correo condicional
def execute_worker_tasks():
    print("\n")
    global last_resp
    global last_scan_time
    global odoo_clients_cache
    global cajera_totals_cache
    
    resp = [] # Inicializar resp antes del bucle
    for olt_id in olt_devices.keys():
        log(f"loop olt #{olt_id}", "info")
        current_resp = CA(olt_devices[olt_id])
        
        # Asignar el nombre de la OLT según su ID
        if str(olt_id) == "1":
            olt_name = "OLT 1 la lago"
        elif str(olt_id) == "2":
            olt_name = "OLT2 Oeste"
        elif str(olt_id) == "3":
            olt_name = "OLT3 Giharro"
        else:
            olt_name = f"OLT {olt_id}"
            
        print(current_resp)
        
        if isinstance(current_resp, list):
            for client in current_resp:
                client['olt_name'] = olt_name
            resp.extend(current_resp)
                
        print("\n")

    # ENRIQUECIMIENTO DE DATOS
    from collections import defaultdict
    cajeras_down = defaultdict(list)
    fsps_down = defaultdict(list)
    
    for client in resp:
        contract = client.get("contract", "")
        # Buscar en caché primero
        if contract in odoo_clients_cache:
            client["nomeclature"] = odoo_clients_cache[contract]["nomeclature"]
            client["fsp"] = odoo_clients_cache[contract]["fsp"]
            client["olt_odoo"] = odoo_clients_cache[contract].get("olt_odoo", "")
        else:
            # Consultar Odoo via middleware para obtener nomenclatura, FSP y OLT
            odoo_res = odoo_request("get-client", {"contract": contract, "sn": "", "identification": ""})
            if odoo_res and odoo_res.get("status") and "data" in odoo_res and odoo_res["data"] is not None:
                odoo_data = odoo_res["data"]
                # Proteger contra None: si nomeclature es None o vacío, usar "Desconocido"
                nom_raw = odoo_data.get("nomeclature")
                client["nomeclature"] = nom_raw if nom_raw else "Desconocido"
                
                frame = odoo_data.get("frame")
                slot = odoo_data.get("slot")
                port = odoo_data.get("olt_port")
                if frame is not None and slot is not None and port is not None:
                    client["fsp"] = f"{frame}/{slot}/{port}"
                else:
                    client["fsp"] = "Desconocido"
                
                # Extraer nombre de OLT tal como lo maneja Odoo
                client["olt_odoo"] = odoo_data.get("olt", "")
                
                # Actualizar caché en caliente
                odoo_clients_cache[contract] = {
                    "nomeclature": client["nomeclature"],
                    "fsp": client["fsp"],
                    "olt_odoo": client["olt_odoo"]
                }
            else:
                client["nomeclature"] = "Desconocido"
                client["fsp"] = "Desconocido"
                client["olt_odoo"] = ""
            
        cajeras_down[client["nomeclature"]].append(client)
        fsps_down[client["fsp"]].append(client)

    db_request(endpoints["empty_alarms"], {})
    db_request(endpoints["add_alarms"], {"alarms": resp})

    current_count = len(resp)
    last_count = len(last_resp)

    # Analizar cajeras con 3+ clientes en corte para incluir en el correo
    cajeras_alertas = {}
    for nom, clients in cajeras_down.items():
        if nom != "Desconocido" and len(clients) >= 3:
            # Obtener total de clientes en esta cajera desde caché o Odoo
            total = cajera_totals_cache.get(nom)
            if not total:
                # Usar el nombre de OLT de Odoo (no el interno) para que la consulta funcione
                olt_odoo_name = clients[0].get("olt_odoo", "")
                log(f"[DEBUG] Consultando get-clients para elemento '{nom}' con olt='{olt_odoo_name}'", "info")
                odoo_res = odoo_request("get-clients", {"element": nom, "fsp": "*", "plan_name": "", "device_type": "", "olt": olt_odoo_name, "state": "Activo"})
                total = len(clients) # Fallback
                if odoo_res and odoo_res.get("status") and isinstance(odoo_res.get("data"), list):
                    total = len(odoo_res["data"])
                    cajera_totals_cache[nom] = total
                    log(f"[DEBUG] get-clients OK: {nom} tiene {total} clientes activos en Odoo", "info")
                else:
                    log(f"[DEBUG] get-clients FALLÓ para {nom}: status={odoo_res.get('status') if odoo_res else 'N/A'}, usando fallback total={total}", "warning")
            
            cajeras_alertas[nom] = {"caidos": len(clients), "total": total, "clients": clients}
            log(f"Alerta Cajera detectada: {nom} con {len(clients)} caídos de {total}", "warning")

    # Guardar cajeras_alertas globalmente para correos programados
    global last_cajeras_alertas
    last_cajeras_alertas = cajeras_alertas

    # Validar Incremento Global (solo después del primer escaneo)
    if last_scan_time is not None:
        diff_time = datetime.now() - last_scan_time
        minutes_passed = int(diff_time.total_seconds() / 60)
        x_tiempo = f"{minutes_passed} minutos"
        
        if current_count >= last_count + 3:
            increment = current_count - last_count
            custom_subject = f"ALERTA DE AVERIA. Incremento de {increment} clientes desconectados en {x_tiempo} (Total: {current_count})"
            log(f"Alerta detectada: {custom_subject}", "warning")
            sending_mail(resp, subject_override=custom_subject, cajeras_alertas=cajeras_alertas)
        
        elif current_count <= last_count - 3:
            decrement = last_count - current_count
            custom_subject = f"RECUPERACIÓN DE CLIENTES. {decrement} clientes reconectados en {x_tiempo} (Total en corte: {current_count})"
            log(f"Recuperación detectada: {custom_subject}", "info")
            sending_mail(resp, subject_override=custom_subject, cajeras_alertas=cajeras_alertas)

    last_resp = resp
    last_scan_time = datetime.now()


def send_scheduled_mail():
    global last_resp
    global last_cajeras_alertas
    log("It's time to send mail.", "info")
    if not last_resp:
        log("No hay clientes en corte. Enviando notificación.", "info")
        send_no_clients_mail()
    else:
        sending_mail(last_resp, cajeras_alertas=last_cajeras_alertas)


def main():
    log("worker running...", "info")

    # Configurar el planificador para ejecutar la recolección cada 15 minutos
    schedule.every(15).minutes.do(execute_worker_tasks)
    log("Tarea programada para ejecutarse cada 15 minutos.", "info")

    # Horas programadas para enviar correo
    mail_send_times = ["07:50AM"] # Solo correo de la mañana

    # Configurar el planificador para enviar correo en las horas especificadas
    for mail_time in mail_send_times:
        # Convertir el formato HH:MM AM/PM a HH:MM para schedule.every().day.at()
        dt_obj = datetime.strptime(mail_time, "%I:%M%p")
        schedule_time = dt_obj.strftime("%H:%M")
        schedule.every().day.at(schedule_time).do(send_scheduled_mail)
        log(f"Correo programado para enviarse a las {mail_time} ({schedule_time})", "info")


    # Ejecutar al menos una vez al iniciar el contenedor para no esperar 30 mins
    log("Ejecutando primera recolección de arranque...", "info")
    try:
        execute_worker_tasks()
        log("Enviando correo con reporte inicial de arranque...", "info")
        send_scheduled_mail()
    except Exception as e:
        log(f"Error en la ejecución de arranque: {e}", "warning")

    # Bucle principal para ejecutar tareas pendientes del planificador
    while True:
        schedule.run_pending()
        time.sleep(1) # Esperar 1 segundo para no consumir CPU


if __name__ == "__main__":
    main()