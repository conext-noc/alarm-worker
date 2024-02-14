from pysnmp.hlapi import *
from helpers.constants.definitions import map_ports,status_types,snmp_down_causes,state_types
from helpers.handlers.failcheck import fail
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


def SNMP_DESC(op,community, host, oid,port,fsp_inicial=""):
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

                if varBind[0].prettyPrint().split('.')[-2] in map_ports:
                    fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                    ont_id = varBind[0].prettyPrint().split('.')[-1]
                    resp = varBind[1].prettyPrint()
                    
                    # print(resp)
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
        # print_fsp(fsp,'success')
                    # print(fsp)
                    
def SNMP_PW(op,community, host, oid,port,fsp_inicial=""):
  
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
                if varBind[0].prettyPrint().split('.')[-2] in map_ports:
                    fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                    ont_id = varBind[0].prettyPrint().split('.')[-1]
                    resp = varBind[1].prettyPrint()
                    if resp != "2147483647":
                        datos[fsp+"-"+ont_id]['Potencia'] = resp[:-2] + "." + resp[-2:]
                    else:
                        datos[fsp+"-"+ont_id]['Potencia'] = "-"
                        
    

def SNMP_STATUS(op,community, host, oid,port,fsp_inicial=""):
  
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
                    
                if resp in status_types:
                    datos[fsp+"-"+ont_id]['Status'] =status_types[resp]

def SNMP_STATE(op,community, host, oid,port,fsp_inicial=""):
  
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
                    
                if resp in state_types:
                    datos[fsp+"-"+ont_id]['State'] =state_types[resp]

#-----------------------SERIAL ONT ------------------------------------
def SNMP_SN(op,community, host, oid,port,fsp_inicial=""):
  
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
                    
                
                datos[fsp+"-"+ont_id]['Sn'] =resp[2:]
                   
                    
#-----------------------LAST_DOWN_CAUSE------------------------------------
def SNMP_LDC(op,community, host, oid,port,fsp_inicial=""):
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
                if varBind[0].prettyPrint().split('.')[-2] in map_ports:
                    fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                    ont_id = varBind[0].prettyPrint().split('.')[-1]
                    resp = varBind[1].prettyPrint()
                    # print(fsp+"-"+ont_id)

                    if resp in snmp_down_causes:
                        datos[fsp+"-"+ont_id]['Last_Down_Cause'] =snmp_down_causes[resp]
                    
#-----------------------LAST_DOWN_TIME------------------------------------
def SNMP_LDT(op,community, host, oid,port,fsp_inicial=""):
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
                if varBind[0].prettyPrint().split('.')[-2] in map_ports:
                    fsp = map_ports[varBind[0].prettyPrint().split('.')[-2]]
                    ont_id = varBind[0].prettyPrint().split('.')[-1]
                    resp = varBind[1].prettyPrint()
                    # print(fsp+"-"+ont_id)
                    año = resp[:6]
                    mes = resp[6:8]
                    dia = resp[8:10]
                    hora = resp[10:12]
                    minuto = resp[12:14]
                    segundo = resp[14:16]

                    
                    datos[fsp+"-"+ont_id]['Last_Down_Time'] = f"{int(año,16)}-{int(mes,16)}-{int(dia,16)} {int(hora,16)}:{int(minuto,16)}:{int(segundo,16)}"
                    
