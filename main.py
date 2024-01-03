import os
import time
from datetime import datetime
from dotenv import load_dotenv
from pysnmp.hlapi import CommunityData, ContextData, UdpTransportTarget
from helpers.handlers.printer import log
from helpers.constants.definitions import olt_devices, endpoints
from helpers.handlers.request import db_request
from scripts.CA import los_clients
from helpers.handlers.mail_sender import send_mail

load_dotenv()


def main():
    clients = []
    log("worker running...", "info")
    count = 1
    while True:
        if bool(
            datetime.now().strftime("%I:%m%p")
            in ["11:30PM", "03:30AM", "07:30AM", "11:30AM", "03:30PM", "07:30PM"]
        ):
            log(f"loop #{count}", "info")
            for olt in range(1, 2):
                start_time = time.time()
                community = CommunityData(os.environ["SNMP_COMMUNITY_DESCRIPCION"])
                target = UdpTransportTarget((olt_devices[str(olt)], 161))
                context = ContextData()
                req = db_request(endpoints["get_ports"], {})["data"] or []
                clts = los_clients(olt, req, community, target, context)
                clients.append(clts)
                end_time = time.time()
                ttl_time = end_time - start_time
                log(
                    f"the ttl amount of time for a given olt [max] is : {ttl_time} secs | {ttl_time/60} min",
                    "info",
                )
            db_request(endpoints["empty_alarms"], {})
            db_request(endpoints["add_alarms"], {"alarms": clients})
            while not bool(
                datetime.now().strftime("%I:%M%p")
                in ["12:00PM", "04:00AM", "08:00AM", "12:00AM", "04:00PM", "08:00PM"]
            ):
                print(
                    f"Waiting for the condition to be met... |{datetime.now().strftime('%I:%M:%S%p')}"
                )
                time.sleep(1)

            send_mail(clients)
            count += 1


if __name__ == "__main__":
    main()
