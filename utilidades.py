def titulo(texto):
    print("\n" + "=" * 52)
    print(f"  {texto}")
    print("=" * 52)
    print("  (escribe 'cancelar' en cualquier campo para volver)\n")


def pedir(mensaje, validar=None, opcional=False):
    """Pide un dato hasta que sea válido. Devuelve None si el usuario escribe 'cancelar'.

    `validar` recibe el texto y devuelve el valor final, o lanza ValueError(mensaje).
    """
    while True:
        texto = input(f"{mensaje}: ").strip()
        if texto.lower() == "cancelar":
            return None
        if not texto and not opcional:
            print("  ✗ Campo obligatorio.")
            continue
        if validar and texto:
            try:
                return validar(texto)
            except ValueError as e:
                print(f"  ✗ {e}")
                continue
        return texto


def elegir(mensaje, opciones):
    """Muestra una lista numerada y devuelve el índice elegido (o None si cancela con 0)."""
    print(f"\n{mensaje}")
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")
    print("  0. Cancelar")
    while True:
        texto = input("Opción: ").strip()
        if texto == "0" or texto.lower() == "cancelar":
            return None
        if texto.isdigit() and 1 <= int(texto) <= len(opciones):
            return int(texto) - 1
        print("  ✗ Opción inválida.")


def confirmar(mensaje):
    while True:
        r = input(f"{mensaje} (s/n): ").strip().lower()
        if r in ("s", "si", "sí"):
            return True
        if r in ("n", "no"):
            return False
        print("  ✗ Responda 's' o 'n'.")


def pausa():
    input("\nPresione Enter para continuar...")
