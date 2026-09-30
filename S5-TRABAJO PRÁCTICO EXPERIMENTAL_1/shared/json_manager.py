import json
import os


class GestorJSON:

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # si el archivo no existe devuelve una lista vacia
        if not os.path.exists(self.ruta):
            return []
        archivo = open(self.ruta, "r", encoding="utf-8")
        datos = json.load(archivo)
        archivo.close()
        return datos

    def guardar(self, datos):
        archivo = open(self.ruta, "w", encoding="utf-8")
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.close()
