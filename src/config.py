import json
from pathlib import Path

# Configuración de rutas base
BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"  # <-- NUEVA RUTA PARA BUSCAR EXCEL

# Archivos de reglas
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"
ARCHIVO_REGLAS_INGRESOS = BASE_DIR / "config" / "reglas_ingresos.json"

# Carpetas de salida
DIR_GASTOS = BASE_DIR / "data" / "output" / "gastos"
DIR_INGRESOS = BASE_DIR / "data" / "output" / "ingresos"
DIR_GASTOS.mkdir(parents=True, exist_ok=True)
DIR_INGRESOS.mkdir(parents=True, exist_ok=True)

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_reglas_ingresos():
    with open(ARCHIVO_REGLAS_INGRESOS, 'r', encoding='utf-8') as f:
        return json.load(f)