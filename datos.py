"""Datos base del sistema y persistencia en JSON."""
import json
import os

# El archivo se guarda en la carpeta raíz del proyecto (un nivel arriba de /funciones)
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(RAIZ_PROYECTO, "bizcotela_datos.json")

ESTADOS = ["Pendiente", "Confirmado", "En preparación", "Listo", "Entregado"]
METODOS_PAGO = ["Yape", "Efectivo"]

# OPCION LUEGO MONTO ADICIONAL LUEGO TAMAÑO (tamaño multiplica)
SABORES = {"Vainilla": 0, "Chocolate": 0, "Naranja": 0, "Zanahoria": 3, "Red velvet": 5}
TAMANOS = {"Pequeño (8 porciones)": 1.0, "Mediano (15 porciones)": 1.6, "Grande (25 porciones)": 2.4}
RELLENOS = {"Manjar": 0, "Crema pastelera": 4, "Fudge": 5, "Fresa": 5, "Lúcuma": 6}
DECORACIONES = {"Sencilla": 0, "Flores de crema": 15, "Fondant": 25, "Personalizada": 35}
CATEGORIAS = ["Torta", "Postre", "Cupcakes", "Sanguchería", "Otro"]

datos = {"clientes": [], "productos": [], "pedidos": [], "contador_pedidos": 0}


def cargar_datos():
    # Se usa update() para no reasignar el diccionario compartido entre módulos
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                datos.update(json.load(f))
        except (json.JSONDecodeError, OSError):
            print("Aviso: no se pudo leer el archivo de datos. Se iniciará vacío.")


def guardar_datos():
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except OSError:
        print("Error: no se pudo guardar la información en el archivo.")
