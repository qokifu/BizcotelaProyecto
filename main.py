import os
import sys

# para importar los datos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from funciones.datos import cargar_datos, guardar_datos
from funciones.clientes import registrar_cliente
from funciones.productos import registrar_producto
from funciones.pedidos import (registrar_pedido, consultar_pedido, actualizar_estado,
                               generar_comprobante, ver_historial)
from funciones.utilidades import confirmar, pausa

OPCIONES = {
    "1": ("Registrar cliente", registrar_cliente),
    "2": ("Registrar producto", registrar_producto),
    "3": ("Registrar pedido", registrar_pedido),
    "4": ("Consultar pedido", consultar_pedido),
    "5": ("Actualizar estado del pedido", actualizar_estado),
    "6": ("Generar comprobante", generar_comprobante),
    "7": ("Ver historial", ver_historial),
}


def mostrar_menu():
    print("\n" + "=" * 52)
    print("        BIZCOTELA CAKES - Pastelería · Desde 2017")
    print("=" * 52)
    print("  MENÚ PRINCIPAL")
    for clave, (texto, _) in OPCIONES.items():
        print(f"  {clave}. {texto}")
    print("  8. Salir")


def main():
    cargar_datos()
    while True:
        mostrar_menu()
        op = input("\nSeleccione una opción: ").strip()
        if op == "8":
            if confirmar("¿Desea cerrar el sistema?"):
                guardar_datos()
                print("¡Hasta pronto!")
                break
        elif op in OPCIONES:
            OPCIONES[op][1]()
            pausa()
        else:
            print("✗ Opción inválida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        guardar_datos()
        print("\nSistema cerrado.")
