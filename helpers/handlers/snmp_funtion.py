from pysnmp.hlapi import *
from helpers.constants.definitions import map_ports,status_types,state_types
from helpers.handlers.failcheck import fail,check_power,check_ldc, check_sn
from helpers.handlers.formatter import date_hex_formatter
# from helpers.shows_progress import print_fsp

datos = {}

OPERATION = {
    "next":nextCmd,
    "get":getCmd,
    "bulk":bulkCmd,
}

def null_datos():
    datos.clear()
    datos = {}
    print(datos)

                    
#-------------------REQUEST MASTER --------------------------------------
def SNMP_Master(op,community, host, oid,port,type_request,fsp_inicial=""):
    iterator = OPERATION[op](
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid+f".{fsp_inicial}")),
        lexicographicMode=False
    )

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                ont_id = varBind[0].prettyPrint().split('.')[-1]
                resp = varBind[1].prettyPrint()

                if type_request=="desc":
                    datos[fsp+"-"+ont_id] = {
                            "fsp": fsp,
                            "ont_id": ont_id,
                            "name": resp,
                            "State": "",
                            "Status": "",
                            "Sn":"",
                            "Potencia": -0,
                            "Last_Down_Cause": "",
                            "Last_Down_Time": "",
                        } 
                elif type_request=="status":
                    if resp in status_types:
                        datos[fsp+"-"+ont_id]['Status'] =status_types[resp]
                elif type_request=="ldc":
                    datos[fsp+"-"+ont_id]['Last_Down_Cause'] = check_ldc(resp)
                elif type_request=="ldt":
                    datos[fsp+"-"+ont_id]['Last_Down_Time'] = date_hex_formatter(resp)
                elif type_request=="state":
                    if resp in state_types:
                        datos[fsp+"-"+ont_id]['State'] =state_types[resp]
                elif type_request=="sn":
                    datos[fsp+"-"+ont_id]['Sn'] = check_sn(resp)
                