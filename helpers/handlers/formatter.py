from helpers.constants.definitions import *

def print_color(text,_type="normal"):
    text_print=""

    text_print = (COLOR2[_type]+text+COLOR2["end"])

    print(text_print)


def date_hex_formatter(hex):

    año = hex[:6]
    mes = hex[6:8]
    dia = hex[8:10]
    hora = hex[10:12]
    minuto = hex[12:14]
    segundo = hex[14:16]

    plain_text = f"{int(año,16)}-{int(mes,16)}-{int(dia,16)} {int(hora,16)}:{int(minuto,16)}:{int(segundo,16)}"
    return plain_text