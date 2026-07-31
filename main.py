import os
import time
import schedule # Importar la librería schedule
from datetime import datetime
from dotenv import load_dotenv
from helpers.handlers.printer import log
from helpers.constants.definitions import olt_devices, endpoints
from helpers.handlers.request import db_request
from scripts.CA import CA,sending_mail
from helpers.handlers.mail_sender import send_mail


global last_resp
global last_scan_time
last_resp = []
last_scan_time = None
load_dotenv()

# Definir la función que contiene la lógica principal y el envío de correo condicional
def execute_worker_tasks():
    print("\n")
    global last_resp
    global last_scan_time
    resp = [] # Inicializar resp antes del bucle
    for olt_id in olt_devices.keys():
        log(f"loop olt #{olt_id}", "info")
        current_resp = CA(olt_devices[olt_id])
        print(current_resp)
        
        if isinstance(current_resp, list):
            resp.extend(current_resp)
                
        print("\n")

    db_request(endpoints["empty_alarms"], {})
    db_request(endpoints["add_alarms"], {"alarms": resp})

    current_count = len(resp)
    last_count = len(last_resp)

    if last_scan_time is not None:
        diff_time = datetime.now() - last_scan_time
        minutes_passed = int(diff_time.total_seconds() / 60)
        x_tiempo = f"{minutes_passed} minutos"
        
        if current_count >= last_count + 5 or current_count >= last_count * 1.05:
            increment = current_count - last_count
            custom_subject = f"ALERTA DE AVERIA. Incremento de {increment} clientes desconectados en {x_tiempo} (Total: {current_count})"
            log(f"Alerta detectada: {custom_subject}", "warning")
            sending_mail(resp, subject_override=custom_subject)

    last_resp = resp
    last_scan_time = datetime.now()
    # print(filtered_clients)


def send_scheduled_mail():
    global last_resp
    log("It's time to send mail.", "info")
    sending_mail(last_resp)


def main():
    log("worker running...", "info")

    # Configurar el planificador para ejecutar la recolección cada 30 minutos
    schedule.every(30).minutes.do(execute_worker_tasks)
    log("Tarea programada para ejecutarse dinámicamente cada 30 minutos.", "info")

    # Horas programadas para enviar correo
    mail_send_times = ["07:45AM","12:15PM","04:15PM"] # Horas para enviar correo

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
    except Exception as e:
        log(f"Error en la ejecución de arranque: {e}", "warning")

    # Bucle principal para ejecutar tareas pendientes del planificador
    while True:
        schedule.run_pending()
        time.sleep(1) # Esperar 1 segundo para no consumir CPU


if __name__ == "__main__":
    main()