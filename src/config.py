import json
from pathlib import Path

# Configuración de rutas base
BASE_DIR = Path(__file__).parent.parent
ARCHIVO_REAL = BASE_DIR / "data" / "input" / "2025-2026.xlsx"

# Archivos de reglas
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"
ARCHIVO_REGLAS_INGRESOS = BASE_DIR / "config" / "reglas_ingresos.json"

NOMBRE_EXTRACTO = ARCHIVO_REAL.stem 

# Carpetas
DIR_GASTOS = BASE_DIR / "data" / "output" / "gastos"
DIR_INGRESOS = BASE_DIR / "data" / "output" / "ingresos"
DIR_GASTOS.mkdir(parents=True, exist_ok=True)
DIR_INGRESOS.mkdir(parents=True, exist_ok=True)

# Rutas de salida para GASTOS
SALIDA_REPORTE = DIR_GASTOS / f"gastos_clasificados_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_PENDIENTES = DIR_GASTOS / f"pendientes_clasificar_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_RESUMEN = DIR_GASTOS / f"resumen_totales_{NOMBRE_EXTRACTO}.xlsx"

# Rutas de salida para INGRESOS
SALIDA_REPORTE_INGRESOS = DIR_INGRESOS / f"ingresos_clasificados_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_PENDIENTES_INGRESOS = DIR_INGRESOS / f"pendientes_clasificar_ingresos_{NOMBRE_EXTRACTO}.xlsx"
SALIDA_RESUMEN_INGRESOS = DIR_INGRESOS / f"resumen_totales_ingresos_{NOMBRE_EXTRACTO}.xlsx"

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_reglas_ingresos():
    with open(ARCHIVO_REGLAS_INGRESOS, 'r', encoding='utf-8') as f:
        return json.load(f)