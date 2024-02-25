import json
import os
import re
import sys
import threading
from queue import Queue
from time import sleep
import unittest
from dotenv import load_dotenv
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    bulkCmd,
    nextCmd,
    SnmpEngine,
)
from helpers.handlers.hex_handler import hex_to_string

load_dotenv()

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.handlers.request import db_request
from helpers.constants.definitions import (
    olt_devices,
    snmp_oid,
    endpoints,
    payload,
    fail_types,
    state_types,
    status_types,
)


class SNMP:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, target):
        self.community = CommunityData(os.environ["SNMP_COMMUNITY"])
        self.target = UdpTransportTarget((target, 161))
        self.context = ContextData()
        self.non_repeaters = 10
        self.max_repetitions = 10

    def execute_bulk(self, oids):
        retry_count = 0
        self.oids = [ObjectType(ObjectIdentity(oid)) for oid in oids]
        data = []

        while retry_count < self.MAX_RETRIES:
            try:
                error_indication, error_status, error_index, values = next(
                    bulkCmd(
                        SnmpEngine(),
                        self.community,
                        self.target,
                        self.context,
                        self.non_repeaters,
                        self.max_repetitions,
                        *self.oids,
                    )
                )
                for value in values:
                    data.append(value.prettyPrint().split(" = ")[1])
                return data
            except Exception as e:
                print(f"Error: {e}. Retrying...")
                retry_count += 1
                sleep(self.RETRY_DELAY)

        print("Max retries reached. Unable to retrieve SNMP data.")
        return None

    def execute_next(self, oid, oid_type, fsp, result_queue):
        values = []
        iterator = nextCmd(
            SnmpEngine(),
            self.community,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False,
            maxRepetitions=self.max_repetitions,
        )
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication or errorStatus:
                continue
            for varBind in varBinds:
                values.append(
                    [
                        varBind.prettyPrint().split(" = ")[1],
                        f'ont-{varBind.prettyPrint().split(" = ")[0].split(".")[-1]}',
                        oid_type,
                        fsp,
                    ]
                )
        iterator.close()
        result_queue.put(values)
        return values

    def execute_iterator(self, oids):
        results = {}
        threads = []
        result_queue = Queue()
        for oid, oid_type, fsp in oids:
            thread = threading.Thread(
                target=self.execute_next, args=(oid, oid_type, fsp, result_queue)
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        while not result_queue.empty():
            oid_values = result_queue.get()
            for value in oid_values:
                data = {
                    value[2]: value[0],
                    "ont": value[1][4:],
                    "fsp": value[3],
                }
                results.setdefault(value[1], {}).update(data)
        return list(results.values())


class TestSnmpBulkCompiler(unittest.TestCase):
    def test_snmp_bulk(self):
        snmp = SNMP("181.232.180.7")
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
        for port in ports:
            if port["is_open"]:
                fsp = f"{port['frame']}/{port['slot']}/{port['port']}"
                devices = snmp.execute_iterator(
                    [
                        (f"{oid}.{port['oid']}", oid_type, fsp)
                        for oid, oid_type in ONT_OIDS
                    ]
                )
                for device in devices:
                    device["contract"] = device["desc"].split(" ")[-1]
                    device["name_1"] = device["desc"].split(" ")[0]
                    device["name_2"] = device["desc"].split(" ")[1]
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
                        alarms.append({
                            "contract": device["contract"],
                            "last_down_time":device["ldt"],
                            "last_down_date":device["ldd"],
                            "last_down_cause":device["ldc"],
                        })

        # values = snmp.execute_bulk(["1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9.4194312192.0", "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1.4194312192.0"])
        # print(values)
        pass


if __name__ == "__main__":
    unittest.main()
