"""Registro de clientes."""
from funciones.datos import datos, guardar_datos
from funciones.utilidades import titulo, pedir


def _validar_dni(t):
    if not t.isdigit() or len(t) != 8:
        raise ValueError("El DNI debe tener 8 dígitos numéricos.")
    if any(c["dni"] == t for c in datos["clientes"]):
        raise ValueError("Ya existe un cliente con ese DNI.")
    return t


def _validar_celular(t):
    if not t.isdigit() or len(t) != 9:
        raise ValueError("El celular debe tener 9 dígitos numéricos.")
    return t


def registrar_cliente():
    titulo("REGISTRAR CLIENTE")
    nombre = pedir("Nombre completo")
    if nombre is None:
        return
    dni = pedir("DNI (8 dígitos)", _validar_dni)
    if dni is None:
        return
    cel = pedir("Celular (9 dígitos)", _validar_celular)
    if cel is None:
        return
    datos["clientes"].append({"nombre": nombre, "dni": dni, "celular": cel})
    guardar_datos()
    print("\n✔ Cliente registrado correctamente.")
