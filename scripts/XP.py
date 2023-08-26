from helpers.handlers import request, port_condition
from helpers.finder.table import clients_table
from helpers.constants import definitions, regex_conditions
from helpers.utils import portHandler
from helpers.finder.port import available_ports

# FUNCTION IMPORT DEFINITIONS
db_request = request.db_request
endpoints = definitions.endpoints
olt_devices = definitions.olt_devices
payload = definitions.payload
vp_count = regex_conditions.vp_count
condition = port_condition.condition
portCounter = portHandler.portCounter
dictToZero = portHandler.dictToZero


def client_ports(comm, command, device):
    lst = []
    clt = {}
    # add to lookup to available ports in db
    lst = available_ports(device)
    payload["lookup_type"] = "CA"
    payload["lookup_value"] = {}
    CLIENTS = []
    RESPONSE = []
    req = db_request(endpoints["get_clients"], payload)
    if req["error"]:
        print("an error occurred")
        return

    clients = req["data"]
    client_list = clients_table(comm, command, lst)

    for client in clients:
        for client_lst in client_list:
            if client["fspi"] == client_lst["fspi"]:
                name = f"{client['name_1']} {client['name_2']} {client['contract']}"
                client["name"] = name
                client["pwr"] = client_lst["pwr"]
                client["status"] = client_lst["status"]
                client["last_down_time"] = client_lst["last_down_time"]
                client["last_down_date"] = client_lst["last_down_date"]
                client["last_down_cause"] = client_lst["last_down_cause"]
                alert = condition(client)
                portCounter(alert, client["plan_name_id"])
                vp_count["1"]["vp_ttl"] += 1
                if alert in ["los", "los+"]:
                    CLIENTS.append(client)

    for clt in CLIENTS:
        last_down_time = str(clt["last_down_time"])
        last_down_date = str(clt["last_down_date"])
        last_down_cause = str(clt["last_down_cause"])
        RESPONSE.append(
            {
                "contract": clt["contract"],
                "last_down_time": last_down_time,
                "last_down_date": last_down_date,
                "last_down_cause": last_down_cause,
            }
        )
    return RESPONSE
