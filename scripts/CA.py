from helpers.constants.definitions import *
from helpers.handlers.formatter import print_color
from helpers.handlers.snmp_funtion import SNMP_DESC,SNMP_PW,SNMP_STATUS
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
table = {}
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
    
    null_datos
    
    return table


        
def CA_snmp(comunity,host,oid_desc,oid_pw,oid_state,oid_last_down_couse,oid_status,oid_last_down_time,oid_sn):
    seguir = True
    while seguir:
        #DESCRIPTION
        thread = threading.Thread(target=SNMP_DESC, args=("next",comunity, host, oid_desc,161))
        thread.start()
        threads.append(thread)
        # #POTENCIA
        # thread = threading.Timer(1,SNMP_PW, args=("next",comunity, host, oid_pw,161,fsp_inicial))
        # thread.start()
        # threads.append(thread)
        #STATUS
        thread = threading.Timer(3,SNMP_STATUS, args=("next",comunity, host, oid_state,161))
        thread.start()
        threads.append(thread)
        #LAST DOWN CAUSE
        thread = threading.Timer(3,SNMP_LDC, args=("next",comunity, host, oid_last_down_couse,161))
        thread.start()
        threads.append(thread)
        # #LAST DOWN TIME
        thread = threading.Timer(3,SNMP_LDT, args=("next",comunity, host, oid_last_down_time,161))
        thread.start()
        threads.append(thread)
        #STATE
        thread = threading.Timer(3,SNMP_STATE, args=("next",comunity, host, oid_status,161))
        thread.start()
        threads.append(thread)
        #SN
        thread = threading.Timer(3,SNMP_SN, args=("next",comunity, host, oid_sn,161))
        thread.start()
        threads.append(thread)
        
        for thread in threads:
            thread.join()

        new_datos = datos
        # table(datos)
        for keys,valores in new_datos.items():
            if valores['State'] == "active" and valores['Status'] == "offline" and valores['Last_Down_Cause'] == "LOSi/LOBi":
                table.append([valores['Nombre'],valores['Sn'],valores['Last_Down_Cause'],valores['Last_Down_Time']])
        seguir = False

        new_datos[:]=[]
        new_datos.clear()
        new_datos ={}

def sending_mail():
    send_mail(table)
