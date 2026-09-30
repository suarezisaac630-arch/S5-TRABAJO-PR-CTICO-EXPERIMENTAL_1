# VISTA: solo menu, input() y print()
from models import CAMPOS
from shared.herramientas import confirmar
from views import *


def pedir_id():
    try:
        return int(input("Id del estudiante: "))
    except ValueError:
        print("El id debe ser un numero")
        return 0


def mostrar_lista(lista):
    if len(lista) == 0:
        print("No hay estudiantes")
    for e in lista:
        print(e.id, "|", e.carnet, "|", e.nombre_completo(), "|", e.email, "| promedio:", e.promedio())


def menu():
    print()
    print("===== SISTEMA DE ESTUDIANTES =====")
    print("1. Crear estudiante")
    print("2. Ver todos")
    print("3. Buscar")
    print("4. Actualizar")
    print("5. Eliminar")
    print("6. Agregar nota")
    print("7. Ver promedio")
    print("8. Materias en comun")
    print("9. Materias ofertadas")
    print("0. Salir")


def main():
    while True:
        menu()
        op = input("Opcion: ")

        if op == "1":
            datos = {}
            for campo in CAMPOS:
                datos[campo] = input(campo + ": ")
            exito, mensaje = crear_estudiante(datos)
            print(mensaje)

        elif op == "2":
            mostrar_lista(obtener_todos())

        elif op == "3":
            texto = input("Buscar (nombre, apellido o carnet): ")
            mostrar_lista(buscar_estudiantes(texto))

        elif op == "4":
            id = pedir_id()
            if obtener_por_id(id) is None:
                print("No existe ese id")
            else:
                print("Deje vacio lo que no quiera cambiar")
                cambios = {}
                for campo in CAMPOS:
                    nuevo = input("Nuevo " + campo + ": ").strip()
                    if nuevo != "":
                        cambios[campo] = nuevo
                exito, mensaje = actualizar_estudiante(id, cambios)
                print(mensaje)

        elif op == "5":
            id = pedir_id()
            e = obtener_por_id(id)
            if e is None:
                print("No existe ese id")
            elif confirmar("Seguro que quiere eliminar a " + e.nombre_completo() + "?"):
                exito, mensaje = eliminar_estudiante(id)
                print(mensaje)

        elif op == "6":
            id = pedir_id()
            materia = input("Materia: ")
            nota = input("Nota (0 a 20): ")
            exito, mensaje = agregar_nota(id, materia, nota)
            print(mensaje)

        elif op == "7":
            e = obtener_por_id(pedir_id())
            if e is None:
                print("No existe ese id")
            else:
                print("Promedio de", e.nombre_completo(), ":", e.promedio())

        elif op == "8":
            print("Primer estudiante")
            a = pedir_id()
            print("Segundo estudiante")
            b = pedir_id()
            exito, resultado = estudiantes_en_comun(a, b)
            if not exito:
                print(resultado)
            elif len(resultado) == 0:
                print("No tienen materias en comun")
            else:
                print("Materias en comun:", sorted(resultado))

        elif op == "9":
            print("Materias:", sorted(materias_ofertadas()))

        elif op == "0":
            print("Adios")
            break

        else:
            print("Opcion no valida")


main()
