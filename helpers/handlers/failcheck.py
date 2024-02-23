from helpers.constants.definitions import ERRORS
from helpers.constants.definitions import snmp_down_causes

def fail(texto):
    
    if texto not in ERRORS:
        return texto
    else:
        return "-"
    
def check_power(power):
    if power != "2147483647":
        f_power = power[:-2] + "." + power[-2:]
        return f_power
    else:
        f_power = "-"
        return f_power
    
def check_ldc(ldc):
    if ldc in snmp_down_causes:
        return snmp_down_causes[ldc]

def check_sn(sn):
    return sn[2:]

