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
import re


load_dotenv()

def CA(olt_ip):
    
    DESCRIPTION = os.getenv("SNMP_COMMUNITY_DESCRIPCION")
    start_time = time.time()
    resp_table = CA_snmp(DESCRIPTION,olt_ip,snmp_oid["descr"],snmp_oid["power"],snmp_oid["status"],snmp_oid["ldc"],snmp_oid["state"],snmp_oid["lddt"],snmp_oid["serial"])
    end_time = time.time()
    ttl_time = end_time - start_time
    log(
                    f"the ttl amount of time for a given olt [olt {olt_ip}] [max] is : {ttl_time:.2f} secs | {(ttl_time/60):.2f} min",
                    "info",
                )
    null_datos()
    
    return resp_table


        
def CA_snmp(comunity,host,oid_desc,oid_pw,oid_state,oid_last_down_couse,oid_status,oid_last_down_time,oid_sn):
    threads = []
    local_table = []
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
                desc = re.split(r"[\s_]+", value['name'])
                name = f"{desc[0]} {desc[1]}"
                try:
                    
                    contract = re.search("000\d{7}", value['name']).group()
                    if(contract == None):
                        contract = re.search("000\d{6}", value['name']).group()
                except AttributeError:
                    contract = "0000000000"
                # contract = value['name'].split()[-1]
                last_down_date_in_days = value['Last_Down_Time'].split()[0]
                last_down_time_in_hours = value['Last_Down_Time'].split()[1]
                local_table.append({
                    "contract":contract,
                    "name":name if len(desc) > 1 else  f"{value['name']}",
                    "last_down_time":last_down_time_in_hours,
                    "last_down_date":last_down_date_in_days,
                    "last_down_cause":value['Last_Down_Cause'],
                })

        seguir = False
    return local_table
        

def sending_mail(data, subject_override=None):
    # Check if data is a list containing a single list
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        send_mail(data[0], subject_override) # Pass the inner list to send_mail
    else:
        send_mail(data, subject_override) # Otherwise, pass data directly

