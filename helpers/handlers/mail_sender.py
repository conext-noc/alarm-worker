import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from helpers.constants.definitions import (
    mail_sender,
    mail_ccs,
    mail_recipients,
    mail_port,
    mail_message,
    mail_server,
    mail_subject,
    mail_table,
    mail_no_clients_subject,
    mail_no_clients_body,
)
from helpers.handlers.printer import log

load_dotenv()

sender_password = os.environ["app_password"]

# Contraseña cargada
def send_mail(clients, subject_override=None, cajeras_alertas=None):
    # DEBUG: Imprimir los datos antes de agrupar y formatear
    log(f"[DEBUG] Iniciando send_mail. Cantidad de clientes a procesar: {len(clients)}", "info")
    log(f"[DEBUG] Clientes data de muestra (primeros 2): {clients[:2]}", "info")
    if cajeras_alertas:
        log(f"[DEBUG] Alertas de cajeras a procesar: {list(cajeras_alertas.keys())}", "info")
    dt = datetime.now().strftime("%d/%m/%Y - %I:%M%p")
    if subject_override:
        subject = subject_override
    else:
        subject = mail_subject + dt
    log(subject, "info")
    t_greet = datetime.now().time().hour
    greet = "Buenos Días" if t_greet < 12 else "Buenas Tardes" if 12 <= t_greet < 18 else "Buenas Noches"
    
    from collections import defaultdict
    grouped = defaultdict(list)
    for client in clients:
        olt = client.get('olt_name', 'OLT Desconocida')
        grouped[olt].append(client)
        
    # PARTE 1: Tabla general de todos los clientes
    html_content = ""
    for olt_name, clist in grouped.items():
        table_rows = ""
        for client in clist:
            elemento = client.get("nomeclature") or "Desconocido"
            fsp = client.get("fsp") or "Desconocido"
            table_rows += f'<tr><td>{client.get("contract", "")}</td><td>{client.get("name", "")}</td><td>{client.get("last_down_time", "")}</td><td>{client.get("last_down_date", "")}</td><td>{client.get("last_down_cause", "")}</td><td>{elemento}</td><td>{fsp}</td></tr>'
        html_content += mail_table.format(olt_name=olt_name, rows=table_rows)

    # PARTE 2: Sección de alertas de cajeras agrupadas (al final del correo)
    if cajeras_alertas:
        html_content += '<hr style="border: 2px solid red; margin: 20px 0;">'
        html_content += '<h2 style="color: red;">⚠️ ALERTAS DE ELEMENTOS EN CORTE</h2>'
        
        for nom, info in cajeras_alertas.items():
            caidos = info["caidos"]
            total = info["total"]
            alert_clients = info["clients"]
            
            html_content += f'<h3 style="color: red;">Elemento {nom} con {caidos} clientes en corte de {total} totales. Validar de manera inmediata.</h3>'
            html_content += '<table border="1" cellpadding="5">'
            html_content += '<tr><th>CONTRATO</th><th>CLIENTE</th><th>HORA DE AVERIA</th><th>DIA DE AVERIA</th><th>CAUSA</th><th>ELEMENTO</th><th>FSP</th></tr>'
            
            for client in alert_clients:
                elemento = client.get("nomeclature") or "Desconocido"
                fsp = client.get("fsp") or "Desconocido"
                html_content += f'<tr><td>{client.get("contract", "")}</td><td>{client.get("name", "")}</td><td>{client.get("last_down_time", "")}</td><td>{client.get("last_down_date", "")}</td><td>{client.get("last_down_cause", "")}</td><td>{elemento}</td><td>{fsp}</td></tr>'
            
            html_content += '</table><br>'

    message = mail_message.format(greet=greet)

    plain_message = MIMEText(message, "plain")
    html_message = MIMEText(html_content, "html")

    msg = MIMEMultipart()
    msg["From"] = mail_sender
    msg["To"] = ", ".join(mail_recipients)
    msg["Cc"] = ", ".join(mail_ccs)
    msg["Subject"] = subject

    msg.attach(plain_message)
    msg.attach(html_message)

    with smtplib.SMTP(mail_server, mail_port) as server:
        server.starttls()
        server.login(mail_sender, sender_password)
        all_recipients = mail_recipients + mail_ccs
        server.sendmail(mail_sender, all_recipients, msg.as_string())
        log("Alarms Mail Sended successfully!", "success")


def send_no_clients_mail():
    """Envía un correo notificando que no se registraron clientes en corte."""
    dt = datetime.now().strftime("%d/%m/%Y - %I:%M%p")
    subject = mail_no_clients_subject + dt
    log(f"Enviando correo de notificación: sin clientes en corte. {dt}", "info")
    
    t_greet = datetime.now().time().hour
    greet = "Buenos Días" if t_greet < 12 else "Buenas Tardes" if 12 <= t_greet < 18 else "Buenas Noches"
    
    html_content = mail_no_clients_body.format(fecha=dt)
    message = mail_message.format(greet=greet)
    
    plain_message = MIMEText(message, "plain")
    html_message = MIMEText(html_content, "html")
    
    msg = MIMEMultipart()
    msg["From"] = mail_sender
    msg["To"] = ", ".join(mail_recipients)
    msg["Cc"] = ", ".join(mail_ccs)
    msg["Subject"] = subject
    
    msg.attach(plain_message)
    msg.attach(html_message)
    
    with smtplib.SMTP(mail_server, mail_port) as server:
        server.starttls()
        server.login(mail_sender, sender_password)
        all_recipients = mail_recipients + mail_ccs
        server.sendmail(mail_sender, all_recipients, msg.as_string())
        log("No-clients notification mail sent successfully!", "success")
