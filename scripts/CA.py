import logging
import os
import time
from helpers.handlers.hex_handler import hex_to_string
from helpers.handlers.request import db_request
from helpers.constants.definitions import (
    endpoints,
    state_types,
    status_types,
    fail_types,
)
from helpers.handlers.snmp_connection import SNMP



def los_clients(olt, olt_id):
    start_time = time.time()
    snmp = SNMP(olt)
    alarms = []
    ONT_OIDS = [
        (os.environ["SNMP_OID_POWER"], "power"),
        (os.environ["SNMP_OID_DESCRIPCION"], "desc"),
        (os.environ["SNMP_OID_LAST_DOWN_CAUSE"], "ldc"),
        (os.environ["SNMP_OID_LAST_DOWN_DT"], "lddt"),
        (os.environ["SNMP_OID_STATUS"], "status"),
        (os.environ["SNMP_OID_STATE"], "state"),
        (os.environ["SNMP_OID_MAC-SERIAL"], "serial"),
    ]
    ports = db_request(endpoints["get_ports"], {})["data"]
    ports = sorted(ports, key=lambda x: x.get("port_id", 0))
    port_len = len([p for p in ports if p["is_open"]])
    elapsed_time = time.time()
    count = 0
    for port in ports:
        if port["is_open"] and int(port["olt"]) == int(olt_id):
            count += 1
            fsp = f"{port['frame']}/{port['slot']}/{port['port']}"
            logging.info(
                f'current fsp : {port["fspo"]:^9} | {count:>4}/{port_len:^4} || {(count/port_len)*100:.2f}% || elapsed time {(elapsed_time - start_time):.2f} s')
            devices = snmp.execute_iterator(
                [(f"{oid}.{port['oid']}", oid_type, fsp) for oid, oid_type in ONT_OIDS]
            )
            for device in devices:
                device["contract"] = device["desc"].split()[-1]
                device["name"] = device["desc"].split(" ")[:-1]
                device["status"] = status_types[device["status"]]
                device["state"] = state_types[device["state"]]
                device["ldc"] = fail_types[device["ldc"]]
                device["lddt"] = hex_to_string(device["lddt"])
                device["ldd"] = device["lddt"][0]
                device["ldt"] = device["lddt"][1]

            for device in devices:
                if (
                    "LOSi/LOBi" == device["ldc"]
                    and "offline" == device["status"]
                    and "active" == device["state"]
                ):
                    alarm = {
                        "contract": device["contract"],
                        "last_down_time": device["ldt"],
                        "last_down_date": device["ldd"],
                        "last_down_cause": device["ldc"],
                    }
                    alarms.append(alarm)

    old_alarms = db_request(endpoints["get_alarms"], {})["data"]

    old_alarms_set = set(tuple(sorted(d.items())) for d in old_alarms)
    alarms_set = set(tuple(sorted(d.items())) for d in alarms)

    # Devices in the new alarms that are not in the old list of alarms
    new_alarms = [dict(tpl) for tpl in alarms_set - old_alarms_set]

    # Devices in both lists of alarms
    updated_alarms = [dict(tpl) for tpl in alarms_set & old_alarms_set]

    # Devices in the old list of alarms that are not in the new list of alarms
    remove_alarms = [dict(tpl) for tpl in old_alarms_set - alarms_set]

    db_request(endpoints["add_alarms"], {"alarms": new_alarms})
    db_request(endpoints["update_alarm"], {"alarms": updated_alarms})
    db_request(endpoints["remove_alarm"], {"alarms": remove_alarms})
    end_time = time.time()
    ttl_time = end_time - start_time
    logging.info(
        f"the ttl amount of time for a given olt [olt {olt_id}] [max] is : {ttl_time:.2f} secs | {(ttl_time/60):.2f} min",
        "info",
    )
