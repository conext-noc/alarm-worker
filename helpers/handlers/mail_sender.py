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


def send_mail(clients, date, time):
    dt = datetime.now().strftime("%d/%m/%Y - %I:%M%p")
    subject = mail_subject + dt
    log(subject, "info")
    table_rows = ""
    for client in clients:
        los_time = f'{client["last_down_date"]}_{client["last_down_time"]}'
        table_rows += f'<tr><td>{client["contract"]}</td><td>{client["name"]}</td><td>{client["plan_name_id"]}</td><td>{los_time}</td></tr>'

    mail_table.format(table_rows)

    plain_message = MIMEText(mail_message, "plain")
    html_message = MIMEText(mail_table, "html")

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
