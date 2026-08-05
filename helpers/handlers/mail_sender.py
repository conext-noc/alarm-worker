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
)
from helpers.handlers.printer import log

load_dotenv()

sender_password = os.environ["app_password"]

# Temporal: Imprimir la contraseña cargada para depuración
print(f"Contraseña cargada (temporal): {sender_password}")

def send_mail(clients, subject_override=None):
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
        
    html_content = ""
    for olt_name, clist in grouped.items():
        table_rows = ""
        for client in clist:
            table_rows += f'<tr><td>{client.get("contract", "")}</td><td>{client.get("name", "")}</td><td>{client.get("last_down_time", "")}</td><td>{client.get("last_down_date", "")}</td><td>{client.get("last_down_cause", "")}</td></tr>'
        html_content += mail_table.format(olt_name=olt_name, rows=table_rows)

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
