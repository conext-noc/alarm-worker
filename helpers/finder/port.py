from helpers.handlers.request import db_request
from helpers.constants.definitions import endpoints

def available_ports(device):
    response = db_request(endpoints['get_ports'],{})
    open_ports = [item for item in response["data"] if item['is_open']]
    response = [{"fsp": f"{item['frame']}/{item['slot']}/{item['port']}"} for item in open_ports if str(item["olt"]) == str(device)]
    return response