# tupla con las respuestas que cuentan como "si"
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def confirmar(pregunta):
    respuesta = input(pregunta + " (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    # tiene que tener un @ y un punto despues del @
    if texto.count("@") != 1:
        return False
    partes = texto.split("@")
    return partes[0] != "" and "." in partes[1]
