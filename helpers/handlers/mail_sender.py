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

sender_password = os.environ["mail_pass"]


def send_mail(clients):
    dt = datetime.now().strftime("%d/%m/%Y - %I:%M%p")
    subject = mail_subject + dt
    log(subject, "info")
    table_rows = ""
    t_greet = datetime.now().time().hour
    greet = "Buenos Días" if t_greet < 12 else "Buenas Tardes" if 12 <= t_greet < 18 else "Buenas Noches"
    for client in clients:
        print()
        table_rows += f'<tr><td>{client["contract"]}</td><td>{client["name"]}</td><td>{client["last_down_time"]}</td><td>{client["last_down_date"]}</td><td>{client["last_down_cause"]}</td></tr>'
    table = mail_table.format(rows=table_rows)
    message = mail_message.format(greet=greet)

    plain_message = MIMEText(message, "plain")
    html_message = MIMEText(table, "html")

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
