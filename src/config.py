import json
from pathlib import Path

# Configuración de rutas base
BASE_DIR = Path(__file__).parent.parent
ARCHIVO_REAL = BASE_DIR / "data" / "input" / "2025-2026.xlsx"
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"

# Extraemos el nombre del archivo original (ej. "2025-2026")
NOMBRE_EXTRACTO = ARCHIVO_REAL.stem 

# Definimos las subcarpetas ---

DIR_GASTOS = BASE_DIR / "data" / "output" / "gastos"
DIR_INGRESOS = BASE_DIR / "data" / "output" / "ingresos"

# : Creamos las carpetas automáticamente si no existen ---
DIR_GASTOS.mkdir(parents=True, exist_ok=True)
DIR_INGRESOS.mkdir(parents=True, exist_ok=True)

# Actualizamos las rutas finales apuntando a sus respectivas subcarpetas
SALIDA_REPORTE = DIR_GASTOS / f"gastos_clasificados_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_PENDIENTES = DIR_GASTOS / f"pendientes_clasificar_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_RESUMEN = DIR_GASTOS / f"resumen_totales_{NOMBRE_EXTRACTO}.xlsx"

SALIDA_INGRESOS = DIR_INGRESOS / f"ingresos_{NOMBRE_EXTRACTO}.xlsx"

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)