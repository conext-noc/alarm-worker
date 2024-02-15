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

# mail_recipients = ["cesar.sanchez@conext.com.ve"]
# mail_ccs = ["ricardo.vera@conext.com.ve"]
mail_recipients = [
    "soporte.oz.1@conext.com.ve",
    "soporte.oz.2@conext.com.ve",
    "dikson.chavez@conext.com.ve",
    "guillermo.rios@conext.com.ve",
    "natali.cera@conext.com.ve",
    "operaciones@conext.com.ve",
]
mail_ccs = ['noc@conext.com.ve']

mail_sender = "noc@conext.com.ve"
mail_server = "smtp.gmail.com"
mail_port = 587
mail_subject = "CLIENTES CON AVERIAS "
mail_table = """
<table border="1" cellpadding="5">
  <tr>
    <th>CONTRATO</th>
    <th>HORA DE AVERIA</th>
    <th>DIA DE AVERIA</th>
    <th>CAUSA</th>
  </tr>
  {rows}
</table>
"""


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
    "state":"1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1",
}


snmp_down_causes = {
    "1": "LOS(Loss of signal)",
    "2": "LOSi/LOBi",
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

ERRORS = {
    "No Such Instance currently exists at this OID",
    "No Such Instance currently exists at this O.ID",
    "No Such Object currently exists at this OID",
    }

COLOR2 = {
    "activated": "\u001b[38;5;2m",
    "suspended": "\u001b[38;5;8m",
    "success": "\u001b[38;5;46m",
    "warning": "\u001b[38;5;202m",
    "off": "\u001b[38;5;196m",
    "fail": "\u001b[31;5;1m", #or \u001b[31;1m
    "info": "\u001b[1;34m",
    "normal": "",
    "end":"\u001b[0m"
}

map_ports = {
    "4194312192" : "0/1/0",       #GPON 0/1/0
    "4194312448":  "0/1/1",       #GPON 0/1/1
    "4194312704":  "0/1/2",       #GPON 0/1/2
    "4194312960":  "0/1/3",       #GPON 0/1/3
    "4194313216":  "0/1/4",       #GPON 0/1/4
    "4194313472":  "0/1/5",       #GPON 0/1/5
    "4194313728":  "0/1/6",       #GPON 0/1/6
    "4194313984":  "0/1/7",       #GPON 0/1/7
    "4194314240":  "0/1/8",       #GPON 0/1/8
    "4194314496":  "0/1/9",       #GPON 0/1/9
    "4194314752": "0/1/10",       #GPON 0/1/10
    "4194315008": "0/1/11",       #GPON 0/1/11
    "4194315264": "0/1/12",       #GPON 0/1/12
    "4194315520": "0/1/13",       #GPON 0/1/13
    "4194315776": "0/1/14",       #GPON 0/1/14
    "4194316032": "0/1/15",       #GPON 0/1/15
    "4194320384": "0/2/0",       #GPON 0/2/0 
    "4194320640":  "0/2/1",       #GPON 0/2/1
    "4194320896":  "0/2/2",       #GPON 0/2/2
    "4194321152":  "0/2/3",       #GPON 0/2/3
    "4194321408":  "0/2/4",       #GPON 0/2/4
    "4194321664":  "0/2/5",       #GPON 0/2/5
    "4194321920":  "0/2/6",       #GPON 0/2/6
    "4194322176":  "0/2/7",       #GPON 0/2/7
    "4194322432":  "0/2/8",       #GPON 0/2/8
    "4194322688":  "0/2/9",       #GPON 0/2/9
    "4194322944": "0/2/10",       #GPON 0/2/10
    "4194323200": "0/2/11",       #GPON 0/2/11
    "4194323456": "0/2/12",       #GPON 0/2/12
    "4194323712": "0/2/13",       #GPON 0/2/13
    "4194323968": "0/2/14",       #GPON 0/2/14
    "4194324224": "0/2/15",       #GPON 0/2/15
    "4194328576":  "0/3/0",       #GPON 0/3/0
    "4194328832":  "0/3/1",       #GPON 0/3/1
    "4194329088":  "0/3/2",       #GPON 0/3/2
    "4194329344":  "0/3/3",       #GPON 0/3/3
    "4194329600":  "0/3/4",       #GPON 0/3/4
    "4194329856":  "0/3/5",       #GPON 0/3/5
    "4194330112":  "0/3/6",       #GPON 0/3/6
    "4194330368":  "0/3/7",       #GPON 0/3/7
    "4194330624":  "0/3/8",       #GPON 0/3/8
    "4194330880":  "0/3/9",       #GPON 0/3/9
    "4194331136": "0/3/10",       #GPON 0/3/10
    "4194331392": "0/3/11",       #GPON 0/3/11
    "4194331648": "0/3/12",       #GPON 0/3/12
    "4194331904": "0/3/13",       #GPON 0/3/13
    "4194332160": "0/3/14",       #GPON 0/3/14
    "4194332416": "0/3/15",       #GPON 0/3/15
    "4194336768":  "0/4/0",       #GPON 0/4/0
    "4194337024":  "0/4/1",       #GPON 0/4/1
    "4194337280":  "0/4/2",       #GPON 0/4/2
    "4194337536":  "0/4/3",       #GPON 0/4/3
    "4194337792":  "0/4/4",       #GPON 0/4/4
    "4194338048":  "0/4/5",       #GPON 0/4/5
    "4194338304":  "0/4/6",       #GPON 0/4/6
    "4194338560":  "0/4/7",       #GPON 0/4/7
    "4194338816":  "0/4/8",       #GPON 0/4/8
    "4194339072":  "0/4/9",       #GPON 0/4/9
    "4194339328": "0/4/10",       #GPON 0/4/10
    "4194339584": "0/4/11",       #GPON 0/4/11
    "4194339840": "0/4/12",       #GPON 0/4/12
    "4194340096": "0/4/13",       #GPON 0/4/13
    "4194340352": "0/4/14",       #GPON 0/4/14
    "4194340608": "0/4/15",       #GPON 0/4/15
    "4194344960":  "0/5/0",       #GPON 0/5/0
    "4194345216":  "0/5/1",       #GPON 0/5/1
    "4194345472":  "0/5/2",       #GPON 0/5/2
    "4194345728":  "0/5/3",       #GPON 0/5/3
    "4194345984":  "0/5/4",       #GPON 0/5/4
    "4194346240":  "0/5/5",       #GPON 0/5/5
    "4194346496":  "0/5/6",       #GPON 0/5/6
    "4194346752":  "0/5/7",       #GPON 0/5/7
    "4194347008":  "0/5/8",       #GPON 0/5/8
    "4194347264":  "0/5/9",       #GPON 0/5/9
    "4194347520": "0/5/10",       #GPON 0/5/10
    "4194347776": "0/5/11",       #GPON 0/5/11
    "4194348032": "0/5/12",       #GPON 0/5/12
    "4194348288": "0/5/13",       #GPON 0/5/13
    "4194348544": "0/5/14",       #GPON 0/5/14
    "4194348800": "0/5/15",       #GPON 0/5/15
    "4194353152":  "0/6/0",       #GPON 0/6/0
    "4194353408":  "0/6/1",       #GPON 0/6/1
    "4194353664":  "0/6/2",       #GPON 0/6/2
    "4194353920":  "0/6/3",       #GPON 0/6/3
    "4194354176":  "0/6/4",       #GPON 0/6/4
    "4194354432":  "0/6/5",       #GPON 0/6/5
    "4194354688":  "0/6/6",       #GPON 0/6/6
    "4194354944":  "0/6/7",       #GPON 0/6/7
    "4194355200":  "0/6/8",       #GPON 0/6/8
    "4194355456":  "0/6/9",       #GPON 0/6/9
    "4194355712": "0/6/10",       #GPON 0/6/10
    "4194355968": "0/6/11",       #GPON 0/6/11
    "4194356224": "0/6/12",       #GPON 0/6/12
    "4194356480": "0/6/13",       #GPON 0/6/13
    "4194356736": "0/6/14",       #GPON 0/6/14
    "4194356992": "0/6/15",       #GPON 0/6/15
    "4194361344":  "0/7/0",       #GPON 0/7/0
    "4194361600":  "0/7/1",       #GPON 0/7/1
    "4194361856":  "0/7/2",       #GPON 0/7/2
    "4194362112":  "0/7/3",       #GPON 0/7/3
    "4194362368":  "0/7/4",       #GPON 0/7/4
    "4194362624":  "0/7/5",       #GPON 0/7/5
    "4194362880":  "0/7/6",       #GPON 0/7/6
    "4194363136":  "0/7/7",       #GPON 0/7/7
    "4194363392":  "0/7/8",       #GPON 0/7/8
    "4194363648":  "0/7/9",       #GPON 0/7/9
    "4194363904": "0/7/10",       #GPON 0/7/10
    "4194364160": "0/7/11",       #GPON 0/7/11
    "4194364416": "0/7/12",       #GPON 0/7/12
    "4194364672": "0/7/13",       #GPON 0/7/13
    "4194364928": "0/7/14",       #GPON 0/7/14
    "4194365184": "0/7/15",       #GPON 0/7/15
    "4194385920": "0/10/0",       #GPON 0/10/0
    "4194386176": "0/10/1",       #GPON 0/10/1
    "4194386432": "0/10/2",       #GPON 0/10/2
    "4194386688": "0/10/3",       #GPON 0/10/3
    "4194386944": "0/10/4",       #GPON 0/10/4
    "4194387200": "0/10/5",       #GPON 0/10/5
    "4194387456": "0/10/6",       #GPON 0/10/6
    "4194387712": "0/10/7",       #GPON 0/10/7
    "4194387968": "0/10/8",       #GPON 0/10/8
    "4194388224": "0/10/9",       #GPON 0/10/9
    "4194388480":"0/10/10",    #GPON 0/10/10
    "4194388736":"0/10/11",    #GPON 0/10/11
    "4194388992":"0/10/12",    #GPON 0/10/12
    "4194389248":"0/10/13",    #GPON 0/10/13
 #  "41943895 # /10/14 "" ,   #GPON 0/10/14
    "4194389760":"0/10/15",    #GPON 0/10/15
    "4194394112": "0/11/0",    #GPON 0/11/0
    "4194394368": "0/11/1",    #GPON 0/11/1
    "4194394624": "0/11/2",    #GPON 0/11/2
    "4194394880": "0/11/3",    #GPON 0/11/3
    "4194395136": "0/11/4",    #GPON 0/11/4
    "4194395392": "0/11/5",    #GPON 0/11/5
    "4194395648": "0/11/6",    #GPON 0/11/6
 #  "4194395904 0/11/7 "" ,    #GPON 0/11/7
    "4194396160": "0/11/8",    #GPON 0/11/8
    "4194396416": "0/11/9",    #GPON 0/11/9
    "4194396672":"0/11/10",    #GPON 0/11/10
    "4194396928":"0/11/11",    #GPON 0/11/11
    "4194397184":"0/11/12",    #GPON 0/11/12
    "4194397440":"0/11/13",    #GPON 0/11/13
    "4194397696":"0/11/14",    #GPON 0/11/14
    "4194397952":"0/11/15",    #GPON 0/11/15
    "4194402304": "0/12/0",    #GPON 0/12/0
    "4194402560": "0/12/1",    #GPON 0/12/1
    "4194402816": "0/12/2",    #GPON 0/12/2
    "4194403072": "0/12/3",    #GPON 0/12/3
    "4194403328": "0/12/4",    #GPON 0/12/4
    # "4194403584": "0/12/5",    #GPON 0/12/5
    # "4194403840": "0/12/6",    #GPON 0/12/6
    # "4194404096": "0/12/7",    #GPON 0/12/7
    # "4194404352": "0/12/8",    #GPON 0/12/8
    # "4194404608": "0/12/9",    #GPON 0/12/9
    # "4194404864": "0/12/10",   #GPON 0/12/10
    # "4194405120": "0/12/11",   #GPON 0/12/11
    # "4194405376": "0/12/12",   #GPON 0/12/12
    # "4194405632": "0/12/13",   #GPON 0/12/13
    # "4194405888": "0/12/14",   #GPON 0/12/14
    # "4194406144": "0/12/15",   #GPON 0/12/15
    "4194410496": "0/13/0",   #GPON 0/13/0
}
