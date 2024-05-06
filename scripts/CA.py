from helpers.constants.definitions import *
from helpers.handlers.formatter import print_color
from helpers.handlers.snmp_funtion import SNMP_Master
from helpers.constants.definitions import *
from helpers.handlers.snmp_funtion import *
from helpers.handlers.mail_sender import send_mail
from dotenv import load_dotenv
import os
import threading
import time
from helpers.handlers.printer import log
from copy import copy


threads = []
table = []
load_dotenv()

def CA(olt_ip):
    
    DESCRIPTION = os.getenv("SNMP_COMMUNITY_DESCRIPCION")
    start_time = time.time()

    resp = CA_snmp(DESCRIPTION,olt_ip,snmp_oid["descr"],snmp_oid["power"],snmp_oid["status"],snmp_oid["ldc"],snmp_oid["state"],snmp_oid["lddt"],snmp_oid["serial"])
    end_time = time.time()
    ttl_time = end_time - start_time
    log(
                    f"the ttl amount of time for a given olt [olt {olt_ip}] [max] is : {ttl_time:.2f} secs | {(ttl_time/60):.2f} min",
                    "info",
                )
    # null_datos
    
    return table


        
def CA_snmp(comunity,host,oid_desc,oid_pw,oid_state,oid_last_down_couse,oid_status,oid_last_down_time,oid_sn):
    seguir = True
    while seguir:
        #DESCRIPTION
        thread = threading.Thread(target=SNMP_Master, args=("next",comunity, host, oid_desc,161,"desc"))
        thread.start()
        threads.append(thread)
        #STATUS
        thread = threading.Timer(5,SNMP_Master, args=("next",comunity, host, oid_state,161,"status"))
        thread.start()
        threads.append(thread)
        #LAST DOWN CAUSE
        thread = threading.Timer(5,SNMP_Master, args=("next",comunity, host, oid_last_down_couse,161,"ldc"))
        thread.start()
        threads.append(thread)
        # #LAST DOWN TIME
        thread = threading.Timer(5,SNMP_Master, args=("next",comunity, host, oid_last_down_time,161,"ldt"))
        thread.start()
        threads.append(thread)
        #STATE
        thread = threading.Timer(5,SNMP_Master, args=("next",comunity, host, oid_status,161,"state"))
        thread.start()
        threads.append(thread)
        #SN
        thread = threading.Timer(5,SNMP_Master, args=("next",comunity, host, oid_sn,161,"sn"))
        thread.start()
        threads.append(thread)
        
        for thread in threads:
            thread.join()

        new_datos = datos
        # table(datos)
        for keys,value in new_datos.items():
            
            if ('State' in value and value['State'] == "active") and value['Status'] == "offline" and value['Last_Down_Cause'] == "LOSi/LOBi":
                name = value['name'].split()[:-1]
                contract = value['name'].split()[-1]
                last_down_date_in_days = value['Last_Down_Time'].split()[0]
                last_down_time_in_hours = value['Last_Down_Time'].split()[1]
                table.append({
                    "contract":contract,
                    "name":f"{name[0]} {name[1]}" if len(name) > 1 else  f"{value['name']}",
                    "last_down_time":last_down_time_in_hours,
                    "last_down_date":last_down_date_in_days,
                    "last_down_cause":value['Last_Down_Cause'],
                })
                # table[keys] += new_datos[keys]

                new_datos[keys].clear()
        seguir = False
        

def sending_mail(data):
    send_mail(data)
    table.clear()
