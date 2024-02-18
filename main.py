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
    while True:
        if bool(
            datetime.now().strftime("%I:%M%p")
            in ["07:30AM", "11:30AM", "03:30PM"]
        ):
            # if True:
            print("\n")
            for olt in range(1, 3):
                log(f"loop olt #{olt}", "info")
                start_time = time.time()
                community = CommunityData(os.environ["SNMP_COMMUNITY_DESCRIPCION"])
                target = UdpTransportTarget((olt_devices[str(olt)], 161))
                context = ContextData()
                req = db_request(endpoints["get_ports"], {})["data"] or []
                clts = los_clients(olt, req, community, target, context)
                clients.extend(clts)
                print("\n")
                end_time = time.time()
                ttl_time = end_time - start_time
                log(
                    f"the ttl amount of time for a given olt [olt {olt}] [max] is : {ttl_time:.2f} secs | {(ttl_time/60):.2f} min",
                    "info",
                )
            clients_set = set()
            filtered_clients = [
                item
                for item in clients
                if (contract := item["contract"]) not in clients_set
                and not clients_set.add(contract)
            ]
            db_request(endpoints["empty_alarms"], {})
            db_request(endpoints["add_alarms"], {"alarms": filtered_clients})
            while not bool(
                datetime.now().strftime("%I%p")
                in [
                    "08AM",
                    "12AM",
                    "04PM",
                ]
            ):
                log(
                    f"Waiting for the condition to be met... |{datetime.now().strftime('%I:%M:%S%p')}",
                    "normal",
                    is_dynamic=True,
                )
                time.sleep(1)
            print("\n")
            # send_mail(filtered_clients)
            print(filtered_clients)
        print(datetime.now().strftime("%I:%M:%S%p"), end="\r")


if __name__ == "__main__":
    main()
