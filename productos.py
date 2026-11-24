"""Registro de productos."""
from funciones.datos import datos, guardar_datos, CATEGORIAS
from funciones.logica import buscar_producto
from funciones.utilidades import titulo, pedir, elegir


def _validar_nombre(t):
    if buscar_producto(t):
        raise ValueError("Ya existe un producto con ese nombre.")
    return t


def _validar_precio(t):
    try:
        precio = float(t.replace(",", "."))
    except ValueError:
        raise ValueError("Ingrese un precio numérico.")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor a 0.")
    return round(precio, 2)


def _validar_stock(t):
    if not t.isdigit():
        raise ValueError("Ingrese un stock entero mayor o igual a 0.")
    return int(t)


def registrar_producto():
    titulo("REGISTRAR PRODUCTO")
    nombre = pedir("Nombre del producto", _validar_nombre)
    if nombre is None:
        return
    idx = elegir("Categoría:", CATEGORIAS)
    if idx is None:
        return
    precio = pedir("Precio base (S/)", _validar_precio)
    if precio is None:
        return
    stock = pedir("Stock", _validar_stock)
    if stock is None:
        return
    datos["productos"].append({"nombre": nombre, "categoria": CATEGORIAS[idx], "precio": precio, "stock": stock})
    guardar_datos()
    print("\n✔ Producto registrado correctamente.")
