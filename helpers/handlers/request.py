import os
import json
from dotenv import load_dotenv
import requests
import urllib3
from helpers.constants import definitions

# Suprimir warnings de SSL para peticiones al middleware
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

domain = definitions.domain
headers = definitions.headers

load_dotenv()


def db_request(endpoint: str, data: dict):
    from helpers.handlers.printer import log
    data["API_KEY"] = os.environ["API_KEY"]
    payload = json.dumps(data)
    url = f"{domain}{endpoint}"
    # log(f"[DEBUG] DB Request -> URL: {url} | Payload: {payload[:200]}...", "info")
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            log(f"[DEBUG] DB Request ERROR <- Status Code: {response.status_code} | Text: {response.text[:200]}", "warning")
            return {
                "error": True,
                "data": None,
                "message": f"Request failed with status code: {response.status_code}",
            }
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        log(f"[DEBUG] DB Request EXCEPTION: {str(e)}", "warning")
        return {"error": True, "message": f"An error occurred: {str(e)}", "data": None}


ODOO_MIDDLEWARE_URL = "https://middleware.conext.net.ve/api/v1/odoo"

def odoo_request(endpoint: str, data: dict):
    """Consulta a Odoo a través del middleware.
    endpoint: 'get-client' o 'get-clients'
    data: diccionario con los campos de búsqueda (contract, element, state, etc.)
    """
    from helpers.handlers.printer import log
    api_key = os.environ.get("ODOO_MIDDLEWARE_API_KEY", "")
    payload = json.dumps({
        "api_key": api_key,
        "data": data
    })
    url = f"{ODOO_MIDDLEWARE_URL}/{endpoint}"
    log(f"[DEBUG] Odoo Request -> Endpoint: {endpoint} | Data: {data}", "info")
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            log(f"[DEBUG] Odoo Request ERROR <- Status Code: {response.status_code} | Text: {response.text[:500]}", "warning")
            return {
                "error": True,
                "data": None,
                "message": f"Odoo request failed with status code: {response.status_code}",
            }
        response_json = response.json()
        log(f"[DEBUG] Odoo Request SUCCESS <- Retornó status: {response_json.get('status')} | Data snippet: {str(response_json.get('data'))[:150]}", "info")
        return response_json
    except requests.RequestException as e:
        log(f"[DEBUG] Odoo Request EXCEPTION: {str(e)}", "warning")
        return {"error": True, "message": f"Odoo error: {str(e)}", "data": None}
