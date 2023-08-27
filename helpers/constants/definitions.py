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
    "get_ports": "/get-ports"
}
olt_devices = {"1": "181.232.180.7", "2": "181.232.180.5", "3": "181.232.180.6"}

mail_message = "Buen día Saludos...\nPor favor comunicarse con los siguientes clientes para corroborar el estado de su servicio, ya que presentan alarma por corte de fibra óptica\n"

mail_recipients = ["ricardo.vera@conext.com.ve"]
mail_ccs = ["ricardo.vera@conext.com.ve"]
# mail_recipients = ['paola.oquendo@conext.com.ve', 'odalys.rangel@conext.com.ve', 'dikson.chavez@conext.com.ve', 'jusmeli.chavez@conext.com.ve', 'nelitza.alvarez@conext.com.ve', 'guillermo.rios@conext.com.ve', 'natali.cera@conext.com.ve',]
# mail_ccs = ['noc@conext.com.ve']

mail_sender = "noc@conext.com.ve"
mail_server = "smtp.gmail.com"
mail_port = 587
mail_subject = "CLIENTES CON AVERIAS {}"
mail_table = """
<table border="1" cellpadding="5">
  <tr>
    <th>CONTRATO</th>
    <th>NOMBRE COMPLETO</th>
    <th>PLAN</th>
    <th>TIEMPO DE AVERIA</th>
  </tr>
  {}
</table>
"""

client_place_holder = {
    "fail": None,
    "name_1": None,
    "name_2": None,
    "contract": None,
    "olt": None,
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "fsp": None,
    "fspi": None,
    "sn": None,
    "last_down_cause": None,
    "state": None,
    "status": None,
    "type": None,
    "ip_address": None,
    "plan_name": None,
    "spid": None,
    "vlan": None,
    "plan": None,
    "provider": None,
    "temp": None,
    "pwr": None,
    "line_profile": None,
    "srv_profile": None,
    "device": None,
    "wan": [{"vlan": None, "spid": None, "plan_name": None, "provider": None}],
}

