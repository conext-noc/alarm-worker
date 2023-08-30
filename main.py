import time
from datetime import datetime
from dotenv import load_dotenv
from helpers.utils.ssh import ssh
from helpers.constants.definitions import olt_devices, endpoints
from helpers.handlers.request import db_request
from scripts.XP import client_ports
from helpers.handlers.mail_sender import send_mail

load_dotenv()


def main():
    clients = []
    count = 1
    print("worker running...")
    while True:
        if bool(datetime.now().strftime("%I%p") in ['12PM', '04AM', '08AM', '12AM', '04PM', '08PM']):
            print(f"loop #{count}")
            for olt in range(1, 2):
                start_time = time.time()
                (comm, command, quit_ssh) = ssh(olt_devices[str(olt)])
                command("scroll 512")
                clts = client_ports(comm, command, str(olt))
                clients.extend(clts)
                quit_ssh()
                end_time = time.time()
                ttl_time = end_time - start_time
                print(
                    f"the ttl amount of time for a given olt [max] is : {ttl_time} secs | {ttl_time/60} min"
                )
            db_request(endpoints["empty_alarms"], {})
            db_request(endpoints["add_alarms"], {"alarms": clients})
            send_mail(clients)
            count += 1


if __name__ == "__main__":
    main()
