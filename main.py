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
last_resp = []
load_dotenv()

# Definir la función que contiene la lógica principal y el envío de correo condicional
def execute_worker_tasks():
    print("\n")
    global last_resp
    resp = [] # Inicializar resp antes del bucle
    for olt in range(1, 3):
        log(f"loop olt #{olt}", "info")
        # community = CommunityData(os.environ["SNMP_COMMUNITY_DESCRIPCION"])
        # Asumiendo que CA devuelve la respuesta que necesitas para resp
        current_resp = CA(olt_devices[str(olt)])
        print(current_resp)
        # if isinstance(current_resp, list): # Verificar si es una lista antes de extender
        #      resp.append(current_resp) # Acumular respuestas si CA devuelve una lista
        # else:
        #      # Si CA no devuelve una lista, manejar según sea necesario.
        #      # Por ahora, simplemente añadir el resultado si no es None.
        #      if current_resp is not None:
        #         resp.append(current_resp)
                
        print("\n")

    # print(resp)
    db_request(endpoints["empty_alarms"], {})
    db_request(endpoints["add_alarms"], {"alarms": resp})

    resp.append(current_resp)
    last_resp = resp
    # print(filtered_clients)


def send_scheduled_mail():
    global last_resp
    log("It's time to send mail.", "info")
    sending_mail(last_resp)


def main():
    log("worker running...", "info")

    # Horas programadas para ejecutar las tareas principales (SNMP, DB, y verificación de envío de correo)
    scheduled_run_times = ["03:30AM","05:30AM","07:30AM","09:30AM","10:30AM","12:00PM","02:30PM","04:00PM","06:30PM","08:30PM","10:30PM","12:00AM"]

    # Configurar el planificador para ejecutar la función en las horas especificadas
    for run_time in scheduled_run_times:
        dt_obj = datetime.strptime(run_time, "%I:%M%p")
        schedule_time = dt_obj.strftime("%H:%M")
        schedule.every().day.at(schedule_time).do(execute_worker_tasks)
        log(f"Tarea programada para ejecutarse a las {run_time}", "info")

    # Horas programadas para enviar correo
    mail_send_times = ["07:45AM","12:15PM","04:15PM"] # Horas para enviar correo

    # Configurar el planificador para enviar correo en las horas especificadas
    for mail_time in mail_send_times:
        # Convertir el formato HH:MM AM/PM a HH:MM para schedule.every().day.at()
        dt_obj = datetime.strptime(mail_time, "%I:%M%p")
        schedule_time = dt_obj.strftime("%H:%M")
        schedule.every().day.at(schedule_time).do(send_scheduled_mail)
        log(f"Correo programado para enviarse a las {mail_time} ({schedule_time})", "info")


    # Bucle principal para ejecutar tareas pendientes del planificador
    while True:
        schedule.run_pending()
        time.sleep(1) # Esperar 1 segundo para no consumir CPU


if __name__ == "__main__":
    main()