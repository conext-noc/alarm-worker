from pysnmp.hlapi import bulkCmd, nextCmd, getCmd

headers = {"Content-Type": "application/json"}
domain = "http://db-api.conext.net.ve"
# domain = "http://localhost:8000"
payload = {"lookup_type": None, "lookup_value": None}
payload_add = {"data": None}
endpoints = {
    "get_client": "/get-client",
    "get_clients": "/get-clients",
    "add_client": "/add-client",
    "update_client": "/update-client",
    "remove_client": "/remove-client",
    "get_plans": "/get-plans",
    "get_alarms": "/get-alarms",
    "add_alarms": "/add-alarms",
    "empty_alarms": "/empty-alarms",
    "get_ports": "/get-ports",
}
olt_devices = {"1": "181.232.180.7", "2": "181.232.180.5", "3": "181.232.180.6"}

mail_message = "{greet}, Saludos...\nPor favor comunicarse con los siguientes clientes para corroborar el estado de su servicio, ya que presentan alarma por corte de fibra óptica\n"

# mail_recipients = ["ricardo.vera@conext.com.ve"]
# mail_ccs = ["ricardo.vera@conext.com.ve"]
mail_recipients = [
    "soporte.oz.1@conext.com.ve",
    "soporte.oz.2@conext.com.ve",
    "dikson.chavez@conext.com.ve",
    "guillermo.rios@conext.com.ve",
    "natali.cera@conext.com.ve",
    "operaciones@conext.com.ve",
]
mail_ccs = ["noc@conext.com.ve"]

mail_sender = "noc@conext.com.ve"
mail_server = "smtp.gmail.com"
mail_port = 587
mail_subject = "CLIENTES CON AVERIAS "
mail_table = """
<table border="1" cellpadding="5">
  <tr>
    <th>CONTRATO</th>
    <th>NOMBRE COMPLETO</th>
    <th>PLAN</th>
    <th>TIEMPO DE AVERIA</th>
  </tr>
  {rows}
</table>
"""

desc_types = {
    "1": "LOS(Loss of signal)",
    "2": "LOSi(Loss of signal for ONUi) or LOBi (Loss of burst for ONUi)",
    "3": "LOFI(Loss of frame of ONUi)",
    "4": "SFI(Signal fail of ONUi)",
    "5": "LOAI(Loss of acknowledge with ONUi)",
    "6": "LOAMI(Loss of PLOAM for ONUi)",
    "7": "deactive ONT fails",
    "8": "deactive ONT success",
    "9": "reset ONT",
    "10": "re-register ONT",
    "11": "pop up fail",
    "13": "dying-gasp",
    "15": "LOKI(Loss of key synch with ONUi)",
    "18": "deactived ONT due to the ring",
    "30": "shut down ONT optical module",
    "31": "reset ONT by ONT command",
    "32": "reset ONT by ONT reset button",
    "33": "reset ONT by ONT software",
    "34": "deactived ONT due to broadcast attack",
    "35": "operator check fail",
    "37": "a rogue ONT detected by itself",
    "-1": "indicates that the query fails.",
}

status_types = {"1": "online", "2": "offline"}

state_types = {"1": "active", "2": "deactivated"}

############################# OIDS & SNMP #############################

snmp_oid = {
    "power": "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4",
    "descr": "1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9",
    "ldc": "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.24",
    "lddt": "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.23",
    "status": ".1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15",
    "serial": ".1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3",
    "state": "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1",
}


snmp_down_causes = {
    "1": "LOS(Loss of signal)",
    "2": "LOSi(Loss of signal for ONUi) or LOBi (Loss of burst for ONUi)",
    "3": "LOFI(Loss of frame of ONUi)",
    "4": "SFI(Signal fail of ONUi)",
    "5": "LOAI(Loss of acknowledge with ONUi)",
    "6": "LOAMI(Loss of PLOAM for ONUi)",
    "7": "deactive ONT fails",
    "8": "deactive ONT success",
    "9": "reset ONT",
    "10": "re-register ONT",
    "11": "pop up fail",
    "13": "dying-gasp",
    "15": "LOKI(Loss of key synch with ONUi)",
    "18": "deactived ONT due to the ring",
    "30": "shut down ONT optical module",
    "31": "reset ONT by ONT command",
    "32": "reset ONT by ONT reset button",
    "33": "reset ONT by ONT software",
    "34": "deactived ONT due to broadcast attack",
    "35": "operator check fail",
    "37": "a rogue ONT detected by itself",
    "-1": "indicates that the query fails.",
}

snmp_status_types = {"1": "online", "2": "offline"}


OPERATION = {
    "next": nextCmd,
    "get": getCmd,
    "bulk": bulkCmd,
}
