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
            in ["07:30AM", "11:30AM", "03:20PM"]
        ):
        # if True:
            print("\n")
            for olt in range(1, 3):
                log(f"loop olt #{olt}", "info")
                # community = CommunityData(os.environ["SNMP_COMMUNITY_DESCRIPCION"])
                CA(olt_devices[str(olt)])
                
                print("\n")
                
            while not bool(
                datetime.now().strftime("%I:%M%p")
                in [
                    "03:23PM"
                ]
            ):
                log(
                    f"Waiting for the condition to be met... |{datetime.now().strftime('%I:%M:%S%p')}",
                    "normal",
                    is_dynamic=True,
                )
                time.sleep(1)
            print("\n")
            sending_mail()
            
            # print(filtered_clients)
        print(datetime.now().strftime("%I:%M:%S%p"), end="\r")


if __name__ == "__main__":
    main()