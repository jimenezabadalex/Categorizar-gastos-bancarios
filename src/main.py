import pandas as pd
import json
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
ARCHIVO_REAL = BASE_DIR / "data" / "input" / "2026.xlsx"
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"
SALIDA_REPORTE = BASE_DIR / "data" / "output" / "gastos_clasificados.xlsx"
SALIDA_PENDIENTES = BASE_DIR / "data" / "output" / "pendientes_clasificar.xlsx"

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def limpiar_datos(ruta):
    df = pd.read_excel(ruta, skiprows=3) # Mantén el skiprows que te funcionó
    
    col_importe = "Importe"
    col_concept = "Concepto"
    
    # Limpieza de importe
    df[col_importe] = df[col_importe].astype(str)
    df[col_importe] = df[col_importe].str.replace(r'[^\d\.,\-]', '', regex=True)
    df[col_importe] = df[col_importe].str.replace('.', '', regex=False)
    df[col_importe] = df[col_importe].str.replace(',', '.', regex=False)
    df[col_importe] = pd.to_numeric(df[col_importe], errors='coerce')
    
    # Filtrar gastos (negativos) y limpiar concepto
    df_gastos = df[df[col_importe] < 0].copy()
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].astype(str).str.upper().str.strip()
    
    return df_gastos

def clasificar_gastos(df, reglas):
    def asignar_categoria(concepto):
        # Busca si alguna palabra clave del JSON está dentro del concepto bancario
        for palabra_clave, categoria in reglas.items():
            if palabra_clave in concepto:
                return categoria
        return "SIN CLASIFICAR" # Si ninguna coincide, la apartamos
    
    # Aplicamos la función a cada fila
    df['Categoria'] = df['Concepto_limpio'].apply(asignar_categoria)
    return df

def ejecutar_pipeline():
    print("🚀 Iniciando categorización de gastos...")
    
    reglas = cargar_reglas()
    df_gastos = limpiar_datos(ARCHIVO_REAL)
    df_clasificado = clasificar_gastos(df_gastos, reglas)
    
    # Aislar lo que no se ha podido clasificar
    df_sin_clasificar = df_clasificado[df_clasificado['Categoria'] == "SIN CLASIFICAR"]
    
    # Agrupar los no clasificados para ver cuáles se repiten más
    pendientes = df_sin_clasificar.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    pendientes = pendientes.sort_values(by='Frecuencia', ascending=False)
    
    # Exportar resultados
    df_clasificado.to_excel(SALIDA_REPORTE, index=False)
    pendientes.to_excel(SALIDA_PENDIENTES, index=False)
    
    print("\n📊 RESUMEN DE EJECUCIÓN:")
    print(f"Total de movimientos analizados: {len(df_clasificado)}")
    print(f"Movimientos clasificados con éxito: {len(df_clasificado) - len(df_sin_clasificar)}")
    print(f"Movimientos SIN CLASIFICAR: {len(df_sin_clasificar)}")
    print("\nArchivos generados en data/output/:")
    print("1. gastos_clasificados.xlsx (El reporte completo)")
    print("2. pendientes_clasificar.xlsx (Tu lista de tareas para añadir al JSON)")

if __name__ == "__main__":
    ejecutar_pipeline()