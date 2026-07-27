def calcular(fsp: str):
    #convertir de fsp a snmp
    value_initial_port = 4194304000
    multipler_slot = 8192
    multiplier_puerto = 256

    f,s,p = fsp.split("/")

    snmp_port_cod = value_initial_port +(int(s) * multipler_slot ) + (int(p) * multiplier_puerto)
    return snmp_port_cod

def calcular_fsp(snmp_port_cod: str):
    #convertir de snmp a fsp
    value_initial_port = 4194304000
    multipler_slot = 8192
    multiplier_puerto = 256

    snmp_port_cod = int(snmp_port_cod) - value_initial_port
    s = snmp_port_cod // multipler_slot
    snmp_port_cod %= multipler_slot
    p = snmp_port_cod // multiplier_puerto

    fsp = f"0/{s}/{p}"
    return fsp