import json
from pathlib import Path

# Configuración de rutas base
BASE_DIR = Path(__file__).parent.parent
ARCHIVO_REAL = BASE_DIR / "data" / "input" / "2025-2026.xlsx"
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"

# Extraemos el nombre del archivo original
NOMBRE_EXTRACTO = ARCHIVO_REAL.stem 

# Rutas de salida
SALIDA_REPORTE = BASE_DIR / "data" / "output" / f"gastos_clasificados_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_PENDIENTES = BASE_DIR / "data" / "output" / f"pendientes_clasificar_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_RESUMEN = BASE_DIR / "data" / "output" / f"resumen_totales_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_INGRESOS = BASE_DIR / "data" / "output" / f"ingresos_{NOMBRE_EXTRACTO}.xlsx"

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)