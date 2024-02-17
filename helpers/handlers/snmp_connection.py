import os
from time import sleep
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    SnmpEngine,
)
from helpers.constants.definitions import OPERATION
from dotenv import load_dotenv

load_dotenv()


class SNMP:
    def __init__(self, target):
        self.community = CommunityData(os.environ["SNMP_COMMUNITY"])
        self.target = UdpTransportTarget((target, 161))
        self.context = ContextData()
        self.non_repeaters = 10
        self.max_repetitions = 10

    def execute(self, operation, oid, init_fsp=""):
        values = []
        iterator = OPERATION[operation](
            SnmpEngine(),
            self.community,
            self.target,
            self.context,
            ObjectType(ObjectIdentity(oid + f".{init_fsp}")),
            lexicographicMode=False,
        )
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
            elif errorStatus:
                print(
                    "%s at %s"
                    % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                    )
                )
            else:
                for varBind in varBinds:
                    values.append(varBind[0].prettyPrint())
        return values
