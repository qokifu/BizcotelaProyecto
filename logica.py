"""Lógica de negocio: cálculos, búsquedas y comprobantes."""
from funciones.datos import datos, SABORES, TAMANOS, RELLENOS, DECORACIONES


def calcular_item(precio_base, sabor, tamano, relleno, decoracion, cantidad):
    """Devuelve (precio_unitario, subtotal)."""
    unitario = precio_base * TAMANOS[tamano] + SABORES[sabor] + RELLENOS[relleno] + DECORACIONES[decoracion]
    unitario = round(unitario, 2)
    return unitario, round(unitario * cantidad, 2)


def buscar_producto(nombre):
    for p in datos["productos"]:
        if p["nombre"].lower() == nombre.strip().lower():
            return p
    return None


def buscar_pedido(codigo):
    codigo = codigo.strip().upper()
    for p in datos["pedidos"]:
        if p["codigo"] == codigo:
            return p
    return None


def texto_comprobante(p):
    linea = "=" * 52
    t = [linea,
         "        BIZCOTELA CAKES - Pastelería y Sangucheria",
         "              Carmen de la Legua Reynoso, Callao",
         linea,
         f"Comprobante / Pedido : {p['codigo']}",
         f"Fecha de registro    : {p['fecha_registro']}",
         f"Fecha de entrega     : {p['fecha_entrega']}",
         "-" * 52,
         f"Cliente  : {p['cliente']}",
         f"DNI      : {p['dni']}",
         f"Celular  : {p['celular']}",
         "-" * 52,
         "DETALLE DEL PEDIDO"]
    for i, it in enumerate(p["items"], 1):
        t.append(f"{i}. {it['producto']}  x{it['cantidad']}")
        t.append(f"   Sabor: {it['sabor']} | Tamaño: {it['tamano']}")
        t.append(f"   Relleno: {it['relleno']} | Decoración: {it['decoracion']}")
        t.append(f"   P. unitario: S/ {it['unitario']:.2f}   Subtotal: S/ {it['subtotal']:.2f}")
    t.append("-" * 52)
    t.append(f"Dedicatoria : {p['dedicatoria'] if p['dedicatoria'] else '(sin dedicatoria)'}")
    t.append(f"Método pago : {p['metodo_pago']}")
    t.append(f"Estado      : {p['estado']}")
    t.append(linea)
    t.append(f"TOTAL A PAGAR: S/ {p['total']:.2f}")
    t.append(linea)
    return "\n".join(t)
