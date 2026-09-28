import pandas as pd

# Importamos las herramientas de nuestros módulos
from config import ARCHIVO_REAL, DIR_INGRESOS
from motor import limpiar_datos

def explorar_ingresos():
    print("🔍 Analizando conceptos únicos de INGRESOS...")
    
    # 1. Usamos nuestro motor para obtener solo los ingresos ya limpios
    _, df_ingresos = limpiar_datos(ARCHIVO_REAL)
    
    # 2. Agrupamos los conceptos únicos y contamos cuántas veces se repiten
    conceptos = df_ingresos['Concepto_limpio'].value_counts().reset_index()
    conceptos.columns = ['Concepto', 'Frecuencia']
    
    # 3. Guardamos la lista en tu carpeta de ingresos
    ruta_salida = DIR_INGRESOS / "conceptos_unicos_ingresos.xlsx"
    conceptos.to_excel(ruta_salida, index=False)
    
    print(f"✅ ¡Listo! Se han encontrado {len(conceptos)} conceptos únicos de ingreso.")
    print(f"📂 Puedes revisarlos aquí: {ruta_salida}")

if __name__ == "__main__":
    explorar_ingresos()
    