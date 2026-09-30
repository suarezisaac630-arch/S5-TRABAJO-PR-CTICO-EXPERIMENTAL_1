# tupla con los campos del estudiante
CAMPOS = ("nombre", "apellido", "email", "carnet")


class Estudiante:

    def __init__(self, id, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self.notas = notas or {}                # diccionario: {"Mate": [18, 20]}
        self.materias = set(materias or [])     # conjunto: no se repiten

    def nombre_completo(self):
        return self.nombre + " " + self.apellido

    def agregar_nota(self, materia, nota):
        self.materias.add(materia)
        self.notas.setdefault(materia, []).append(nota)

    def promedio(self):
        todas = []
        for lista in self.notas.values():
            todas.extend(lista)
        if len(todas) == 0:
            return 0
        return round(sum(todas) / len(todas), 2)

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": sorted(self.materias),   # el set se guarda como lista
        }


def desde_diccionario(d):
    return Estudiante(d["id"], d["nombre"], d["apellido"], d["email"],
                      d["carnet"], d["notas"], d["materias"])
