import logging
import os
import threading
from time import sleep
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    SnmpEngine,
    nextCmd,bulkCmd
)
from dotenv import load_dotenv
from queue import Queue

load_dotenv()

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
                logging.error(f"Error: {e}. Retrying...")
                retry_count += 1
                sleep(self.RETRY_DELAY)

        logging.error("Max retries reached. Unable to retrieve SNMP data.")
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
                logging.error(f"errorIndication : {errorIndication} | errorStatus : {errorStatus} | errorIndex : {errorIndex}")
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

