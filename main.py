import logging
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
from helpers.handlers.printer import log
from helpers.constants.definitions import olt_devices, endpoints, log_file, log_date_format, log_format
from helpers.handlers.request import db_request
from scripts.CA import los_clients
from helpers.handlers.mail_sender import send_mail

load_dotenv()


from scripts.CA import los_clients


class MainThread(threading.Thread):
    def run(self):
        log("main thread running...", "info")
        while not bool(
            datetime.now().strftime("%I%p") in ["07:45AM", "12:15PM", "04:15PM"]
        ):
            log(
                f"Waiting for the condition to be met... |{datetime.now().strftime('%I:%M:%S%p')}",
                "normal",
                is_dynamic=True,
            )
            time.sleep(1)
        print("\n")
        alarms = db_request(endpoints["get_alarms"], {})["data"]
        filtered_clients = []
        for alarm in alarms:
            client = db_request(
                endpoints["get_client"],
                {
                    "lookup_type": "C",
                    "lookup_value": {"contract": alarm["contract"], "olt": "*"},
                },
            )["data"]
            filtered_clients.append(client)

        send_mail(filtered_clients)


class WorkerThread(threading.Thread):
    def run(self):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format=log_format,
            datefmt=log_date_format,
        )
        logging.info("worker running...")
        while True:
            for device in range(1, 3):
                logging.info(f"loop olt #{device}")
                olt = olt_devices[str(device)]
                los_clients(olt, device)
                time.sleep(2 * 60 * 60)  # hours * min * secs = 7200 secs === 2 hours


if __name__ == "__main__":
    th1 = MainThread()
    th1.start()
    th2 = WorkerThread()
    th2.start()
