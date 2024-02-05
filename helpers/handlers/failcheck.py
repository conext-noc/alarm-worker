from helpers.constants.definitions import ERRORS

def fail(texto):
    
    if texto not in ERRORS:
        return texto
    else:
        return "-"