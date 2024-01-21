import os
import string
import time
from helpers.constants.definitions import status_types, desc_types, payload, endpoints, state_types
from dotenv import load_dotenv
from helpers.handlers.hex_handler import hex_to_string
from helpers.handlers.printer import log
from helpers.handlers.request import db_request
from pysnmp.hlapi import (
    ObjectType,
    ObjectIdentity,
    bulkCmd,
    SnmpEngine,
)

load_dotenv()


def los_clients(device, port_list, community, target, context):
    non_repeaters = 10
    max_repetitions = 10
    CLIENTS = []
    count = 0
    start_time = time.time()
    for port in port_list:
        if port["is_open"] and str(device) == str(port["olt"]):
            count += 1
            payload["lookup_type"] = "VP"
            payload["lookup_value"] = {
                "fsp": port["fspo"].split("-")[0],
                "olt": port["fspo"].split("-")[1],
            }
            port_len = len([p for p in port_list if p["is_open"]])
            elapsed_time = time.time()
            log(f'current fsp : {port["fspo"]:^9} | {count:>4}/{port_len:^4} || {(count/port_len)*100:.2f}% || elapsed time {(elapsed_time - start_time):.2f} s', "info", is_dynamic=True)
            clients_req = db_request(endpoints["get_clients"], payload)["data"]
            for client in clients_req:
                ont_id = "" if client["onu_id"] == 0 else f".{int(client['onu_id'])-1}"
                oid_1 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_DESCRIPCION"] + f'{port["oid"]}{ont_id}'
                    )
                )
                oid_2 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_STATUS"] + f'{port["oid"]}{ont_id}'
                    )
                )
                oid_3 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_MAC-SERIAL"] + f'{port["oid"]}{ont_id}'
                    )
                )
                oid_4 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_POWER"] + f'{port["oid"]}{ont_id}'
                    )
                )
                oid_5 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_LAST_DOWN_CAUSE"]
                        + f'{port["oid"]}{ont_id}'
                    )
                )
                oid_6 = ObjectType(
                    ObjectIdentity(
                        "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.23."
                        + f'{port["oid"]}{ont_id}'
                    )
                )  # hwGponDeviceOntControlLastDownTime
                oid_7 = ObjectType(
                    ObjectIdentity(
                        os.environ["SNMP_OID_STATE"]
                        + f'{port["oid"]}{ont_id}'
                    )
                )  # hwGponDeviceOntState

                error_indication, error_status, error_index, var_bind_table = next(
                    bulkCmd(
                        SnmpEngine(),
                        community,
                        target,
                        context,
                        non_repeaters,
                        max_repetitions,
                        oid_1,
                        oid_2,
                        oid_3,
                        oid_4,
                        oid_5,
                        oid_6,
                        oid_7,
                    )
                )
                # print(error_indication, error_status, error_index)
                if error_indication is not None:
                    continue
                descr = f"{var_bind_table[0]}".split(" = ")[1]
                ont = {
                    "frame": client["frame"],
                    "slot": client["slot"],
                    "port": client["port"],
                    "fsp": client["fsp"],
                    "fspi": client["fspi"],
                    "ont_id": client["onu_id"],
                    "ont_descr": descr,
                    "name_1": descr.split(" ")[0],
                    "name_2": descr.split(" ")[1],
                    "contract": descr.split(" ")[-1],
                    "ont_status": status_types[f"{var_bind_table[1]}".split(" = ")[1]],
                    "ont_serial": f"{var_bind_table[2]}".split(" = ")[1].replace(
                        "0x", ""
                    ),
                    "ont_state": state_types[str(var_bind_table[6][1].prettyPrint())],
                    "ont_power": int(f"{var_bind_table[3]}".split(" = ")[1]) / 100,
                    "ont_ldc": desc_types[f"{var_bind_table[4]}".split(" = ")[1]],
                    "ont_ldd": hex_to_string(var_bind_table[5][1].prettyPrint())[0],
                    "ont_ldt": hex_to_string(var_bind_table[5][1].prettyPrint())[1],
                    "plan_name_id": client["plan_name_id"],
                    "spid": client["spid"],
                    "device": client["device"]
                    .replace("EchoLife", "")
                    .translate({ord(c): None for c in string.whitespace}),
                }
                if (
                    ont["ont_status"] == "offline"
                    and ont["ont_state"] == "active"
                    and "LOS" in ont["ont_ldc"]
                ):
                    CLIENTS.append(
                        {
                            "contract": ont["contract"],
                            "last_down_time": ont["ont_ldt"],
                            "last_down_date": ont["ont_ldd"],
                            "last_down_cause": ont["ont_ldc"],
                            "name": f'{ont["name_1"]} {ont["name_2"]}',
                            "plan_name_id": ont["plan_name_id"],
                        }
                    )
    return CLIENTS
