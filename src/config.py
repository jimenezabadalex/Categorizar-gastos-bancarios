import json
from pathlib import Path

# Configuración de rutas base
BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"

# Archivos de reglas
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"
ARCHIVO_REGLAS_INGRESOS = BASE_DIR / "config" / "reglas_ingresos.json"

# Archivos de reglas demo
ARCHIVO_REGLAS_DEMO = BASE_DIR / "config" / "reglas.json.example"
ARCHIVO_REGLAS_INGRESOS_DEMO = BASE_DIR / "config" / "reglas_ingresos.json.example"

# Carpetas de salida
DIR_GASTOS = BASE_DIR / "data" / "output" / "gastos"
DIR_INGRESOS = BASE_DIR / "data" / "output" / "ingresos"
DIR_GASTOS.mkdir(parents=True, exist_ok=True)
DIR_INGRESOS.mkdir(parents=True, exist_ok=True)

def cargar_reglas(es_demo=False):
    ruta = ARCHIVO_REGLAS_DEMO if es_demo else ARCHIVO_REGLAS
    
    # Si el archivo real no existe (ej. un reclutador que acaba de clonar), forzamos el demo
    if not ruta.exists():
        ruta = ARCHIVO_REGLAS_DEMO
        
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_reglas_ingresos(es_demo=False):
    ruta = ARCHIVO_REGLAS_INGRESOS_DEMO if es_demo else ARCHIVO_REGLAS_INGRESOS
    
    if not ruta.exists():
        ruta = ARCHIVO_REGLAS_INGRESOS_DEMO
        
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)