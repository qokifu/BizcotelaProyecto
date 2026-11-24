"""Pedidos: registrar, consultar, actualizar estado, comprobantes e historial."""
import os
from datetime import datetime

from funciones.datos import (datos, guardar_datos, RAIZ_PROYECTO, ESTADOS, METODOS_PAGO,
                             SABORES, TAMANOS, RELLENOS, DECORACIONES)
from funciones.logica import calcular_item, buscar_producto, buscar_pedido, texto_comprobante
from funciones.utilidades import titulo, pedir, elegir, confirmar


def _elegir_opcion(mensaje, diccionario, mostrar_extra=True):
    """Elige una clave de un diccionario de opciones. Devuelve la clave o None."""
    claves = list(diccionario)
    etiquetas = [f"{k} (+S/ {v})" if mostrar_extra and v else k for k, v in diccionario.items()]
    idx = elegir(mensaje, etiquetas)
    return None if idx is None else claves[idx]


def _mostrar_items(items):
    if not items:
        print("\n  (el pedido aún no tiene ítems)")
        return
    print("\n  ÍTEMS DEL PEDIDO")
    for i, it in enumerate(items, 1):
        print(f"  {i}. {it['producto']} x{it['cantidad']} | {it['sabor']} | {it['tamano']} | "
              f"{it['relleno']} | {it['decoracion']} -> S/ {it['subtotal']:.2f}")
    print(f"  TOTAL: S/ {sum(i['subtotal'] for i in items):.2f}")


def _agregar_item(items):
    idx = elegir("Producto:", [f"{p['nombre']} - S/ {p['precio']:.2f} (stock: {p['stock']})"
                               for p in datos["productos"]])
    if idx is None:
        return
    prod = datos["productos"][idx]

    def validar_cant(t):
        if not t.isdigit() or int(t) <= 0:
            raise ValueError("Ingrese una cantidad entera mayor a 0.")
        cant = int(t)
        ya_pedido = sum(i["cantidad"] for i in items if i["producto"] == prod["nombre"])
        if cant + ya_pedido > prod["stock"]:
            raise ValueError(f"Solo hay {prod['stock']} unidades de '{prod['nombre']}' disponibles.")
        return cant

    cant = pedir("Cantidad", validar_cant)
    if cant is None:
        return
    sabor = _elegir_opcion("Sabor:", SABORES)
    if sabor is None:
        return
    tamano = _elegir_opcion("Tamaño:", TAMANOS, mostrar_extra=False)
    if tamano is None:
        return
    relleno = _elegir_opcion("Relleno:", RELLENOS)
    if relleno is None:
        return
    deco = _elegir_opcion("Decoración:", DECORACIONES)
    if deco is None:
        return

    unit, sub = calcular_item(prod["precio"], sabor, tamano, relleno, deco, cant)
    items.append({"producto": prod["nombre"], "sabor": sabor, "tamano": tamano, "relleno": relleno,
                  "decoracion": deco, "cantidad": cant, "unitario": unit, "subtotal": sub})
    print(f"\n✔ Ítem agregado. Subtotal: S/ {sub:.2f}")


def registrar_pedido():
    titulo("REGISTRAR PEDIDO")
    if not datos["clientes"]:
        print("Primero debe registrar al menos un cliente.")
        return
    if not datos["productos"]:
        print("Primero debe registrar al menos un producto.")
        return

    idx = elegir("Cliente:", [f"{c['nombre']} - {c['dni']}" for c in datos["clientes"]])
    if idx is None:
        return
    cliente = datos["clientes"][idx]

    items = []
    while True:
        _mostrar_items(items)
        op = elegir("¿Qué desea hacer?", ["Agregar ítem", "Quitar ítem", "Continuar con el pedido"])
        if op is None:
            print("Se canceló el registro del pedido.")
            return
        if op == 0:
            _agregar_item(items)
        elif op == 1:
            if not items:
                print("  ✗ No hay ítems para quitar.")
                continue
            n = elegir("Ítem a quitar:", [f"{i['producto']} x{i['cantidad']}" for i in items])
            if n is not None:
                del items[n]
        else:
            if not items:
                print("  ✗ Agregue al menos un producto al pedido.")
                continue
            break

    dedicatoria = pedir("Dedicatoria (Enter para omitir)", opcional=True)
    if dedicatoria is None:
        return

    def validar_fecha(t):
        try:
            fecha = datetime.strptime(t, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Ingrese la fecha con el formato dd/mm/aaaa.")
        if fecha.date() < datetime.now().date():
            raise ValueError("La fecha de entrega no puede ser anterior a hoy.")
        return fecha

    fecha = pedir("Fecha de entrega (dd/mm/aaaa)", validar_fecha)
    if fecha is None:
        return
    pago = elegir("Método de pago:", METODOS_PAGO)
    if pago is None:
        return

    pedido = {
        "codigo": f"PED-{datos['contador_pedidos'] + 1:04d}",
        "cliente": cliente["nombre"], "dni": cliente["dni"], "celular": cliente["celular"],
        "items": [dict(i) for i in items],
        "dedicatoria": dedicatoria,
        "fecha_entrega": fecha.strftime("%d/%m/%Y"),
        "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "metodo_pago": METODOS_PAGO[pago],
        "total": round(sum(i["subtotal"] for i in items), 2),
        "estado": ESTADOS[0],
    }
    print("\n" + texto_comprobante(pedido))
    if confirmar("\n¿Desea registrar este pedido?"):
        datos["contador_pedidos"] += 1
        for i in items:  # descontar stock
            buscar_producto(i["producto"])["stock"] -= i["cantidad"]
        datos["pedidos"].append(pedido)
        guardar_datos()
        print(f"\n✔ Pedido {pedido['codigo']} registrado correctamente.")
    else:
        print("Se canceló el registro del pedido.")


def consultar_pedido():
    titulo("CONSULTAR PEDIDO")
    codigo = pedir("Código del pedido (ej. PED-0001)")
    if codigo is None:
        return
    p = buscar_pedido(codigo)
    if p:
        print("\n" + texto_comprobante(p))
    else:
        print("Pedido no encontrado.")


def actualizar_estado():
    titulo("ACTUALIZAR ESTADO DEL PEDIDO")
    if not datos["pedidos"]:
        print("No existen pedidos registrados.")
        return
    idx = elegir("Pedido:", [f"{p['codigo']} - {p['cliente']} [{p['estado']}]" for p in datos["pedidos"]])
    if idx is None:
        return
    p = datos["pedidos"][idx]
    print(f"\nEstado actual: {p['estado']}")
    n = elegir("Nuevo estado:", ESTADOS)
    if n is None:
        return
    p["estado"] = ESTADOS[n]
    guardar_datos()
    print(f"\n✔ El pedido {p['codigo']} ahora está '{p['estado']}'.")


def generar_comprobante():
    titulo("GENERAR COMPROBANTE")
    if not datos["pedidos"]:
        print("No existen pedidos registrados.")
        return
    idx = elegir("Seleccione el pedido:", [f"{p['codigo']} - {p['cliente']}" for p in datos["pedidos"]])
    if idx is None:
        return
    p = datos["pedidos"][idx]
    texto = texto_comprobante(p)
    print("\n" + texto)
    if confirmar("\n¿Guardar comprobante como .txt?"):
        carpeta = os.path.join(RAIZ_PROYECTO, "comprobantes")
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"comprobante_{p['codigo']}.txt")
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(texto)
            print(f"✔ Comprobante guardado en: {ruta}")
        except OSError:
            print("Error: no se pudo guardar el comprobante.")


def ver_historial():
    titulo("HISTORIAL DE PEDIDOS")
    if not datos["pedidos"]:
        print("No existen pedidos registrados.")
        return
    print(f"{'Código':<10}{'Cliente':<26}{'Entrega':<12}{'Total':>10}  {'Estado'}")
    print("-" * 72)
    for p in reversed(datos["pedidos"]):
        print(f"{p['codigo']:<10}{p['cliente'][:24]:<26}{p['fecha_entrega']:<12}"
              f"{'S/ ' + format(p['total'], '.2f'):>10}  {p['estado']}")
    codigo = pedir("\nCódigo para ver detalle (Enter para volver)", opcional=True)
    if codigo:
        p = buscar_pedido(codigo)
        print("\n" + texto_comprobante(p) if p else "Pedido no encontrado.")
