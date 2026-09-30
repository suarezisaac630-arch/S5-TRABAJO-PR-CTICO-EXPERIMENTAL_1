# CONTROLADOR: las reglas. Aqui no hay print() ni input()
import os
from models import Estudiante, desde_diccionario, CAMPOS
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

carpeta = os.path.dirname(os.path.abspath(__file__))
gestor = GestorJSON(os.path.join(carpeta, "data", "estudiantes.json"))


def carnets_registrados(excepto_id=0):
    # conjunto con los carnets que ya existen
    carnets = set()
    for r in gestor.leer():
        if r["id"] != excepto_id:
            carnets.add(r["carnet"].lower())
    return carnets


def siguiente_id():
    mayor = 0
    for r in gestor.leer():
        if r["id"] > mayor:
            mayor = r["id"]
    return mayor + 1


# CREATE
def crear_estudiante(datos):
    for campo in CAMPOS:
        if datos[campo].strip() == "":
            return False, "El campo " + campo + " esta vacio"
    if not es_email_valido(datos["email"]):
        return False, "El email no es valido"
    if datos["carnet"].lower() in carnets_registrados():
        return False, "Ese carnet ya existe"

    e = Estudiante(siguiente_id(), datos["nombre"], datos["apellido"], datos["email"], datos["carnet"])
    lista = gestor.leer()
    lista.append(e.a_diccionario())
    gestor.guardar(lista)
    return True, "Estudiante creado con id " + str(e.id)


# READ
def obtener_todos():
    lista = []
    for r in gestor.leer():
        lista.append(desde_diccionario(r))
    return lista


def obtener_por_id(id):
    for e in obtener_todos():
        if e.id == id:
            return e
    return None


# SEARCH
def buscar_estudiantes(texto):
    texto = texto.lower()
    encontrados = []
    for e in obtener_todos():
        if texto in e.nombre.lower() or texto in e.apellido.lower() or texto in e.carnet.lower():
            encontrados.append(e)
    return encontrados


# UPDATE
def actualizar_estudiante(id, cambios):
    if "email" in cambios and not es_email_valido(cambios["email"]):
        return False, "El email no es valido"
    if "carnet" in cambios and cambios["carnet"].lower() in carnets_registrados(id):
        return False, "Ese carnet ya existe"

    lista = gestor.leer()
    for r in lista:
        if r["id"] == id:
            r.update(cambios)
            gestor.guardar(lista)
            return True, "Estudiante actualizado"
    return False, "No existe ese id"


# DELETE
def eliminar_estudiante(id):
    lista = gestor.leer()
    nueva = []
    for r in lista:
        if r["id"] != id:
            nueva.append(r)
    if len(nueva) == len(lista):
        return False, "No existe ese id"
    gestor.guardar(nueva)
    return True, "Estudiante eliminado"


# NOTAS
def agregar_nota(id, materia, nota):
    if materia.strip() == "":
        return False, "La materia esta vacia"
    try:
        nota = float(nota)
    except ValueError:
        return False, "La nota debe ser un numero"
    if nota < 0 or nota > 20:
        return False, "La nota debe estar entre 0 y 20"

    lista = gestor.leer()
    for i in range(len(lista)):
        if lista[i]["id"] == id:
            e = desde_diccionario(lista[i])
            e.agregar_nota(materia.strip(), nota)
            lista[i] = e.a_diccionario()
            gestor.guardar(lista)
            return True, "Nota agregada"
    return False, "No existe ese id"


def materias_ofertadas():
    # union de todos los conjuntos de materias
    todas = set()
    for e in obtener_todos():
        todas = todas | e.materias
    return todas


def estudiantes_en_comun(id_a, id_b):
    a = obtener_por_id(id_a)
    b = obtener_por_id(id_b)
    if a is None or b is None:
        return False, "Alguno de los dos ids no existe"
    return True, a.materias & b.materias      # interseccion
