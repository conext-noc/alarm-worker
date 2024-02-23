import os
import time
from datetime import datetime
from dotenv import load_dotenv
from helpers.handlers.printer import log
from helpers.constants.definitions import olt_devices, endpoints
from helpers.handlers.request import db_request
from scripts.CA import CA,sending_mail
from helpers.handlers.mail_sender import send_mail



load_dotenv()


def main():
    clients = []
    log("worker running...", "info")
    while True:
        if bool(
            datetime.now().strftime("%I:%M%p")
            in ["03:30AM","05:30AM","07:30AM","09:30AM","10:30AM","12:00PM","02:30PM","04:00PM","06:30PM","08:30PM","10:30PM","12:00AM","04:41PM"]
        ):
        # if True:
            print("\n")
            for olt in range(1, 3):
                log(f"loop olt #{olt}", "info")
                # community = CommunityData(os.environ["SNMP_COMMUNITY_DESCRIPCION"])
                resp = CA(olt_devices[str(olt)])
                print("\n")
            # print(resp)
            db_request(endpoints["empty_alarms"], {})
            db_request(endpoints["add_alarms"], {"alarms": resp})
            while not bool(
                datetime.now().strftime("%I:%M%p")
                in [
                    "07:45AM","12:15PM","04:15PM"
                ]
            ):
                log(
                    f"Waiting for the condition to be met... |{datetime.now().strftime('%I:%M:%S%p')}",
                    "normal",
                    is_dynamic=True,
                )
                time.sleep(1)
            print("\n")
            print(resp)
            sending_mail(resp)
            
            
            # print(filtered_clients)
        print(datetime.now().strftime("%I:%M:%S%p"), end="\r")


if __name__ == "__main__":
    main()