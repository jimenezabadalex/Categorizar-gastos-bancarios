import pandas as pd
import json
import unicodedata
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent.parent
ARCHIVO_REAL = BASE_DIR / "data" / "input" / "2026.xlsx"
ARCHIVO_REGLAS = BASE_DIR / "config" / "reglas.json"

SALIDA_REPORTE = BASE_DIR / "data" / "output" / "gastos_clasificados.xlsx"
SALIDA_PENDIENTES = BASE_DIR / "data" / "output" / "pendientes_clasificar.xlsx"
SALIDA_RESUMEN = BASE_DIR / "data" / "output" / "resumen_totales.xlsx"

def cargar_reglas():
    with open(ARCHIVO_REGLAS, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalizar_texto(texto):
    """
    Convierte el texto a mayúsculas (controlando minúsculas/mayúsculas) 
    y elimina todas las tildes y diéresis.
    """
    # 1. Pone todo en mayúsculas y quita espacios de los bordes
    texto = str(texto).upper().strip()
    
    # 2. Descompone y elimina acentos/tildes
    texto = unicodedata.normalize('NFD', texto)
    texto_limpio = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    
    return texto_limpio

def limpiar_datos(ruta):
    df = pd.read_excel(ruta, skiprows=3)
    
    col_importe = "Importe"
    col_concept = "Concepto"
    
    # Limpieza matemática del importe
    df[col_importe] = df[col_importe].astype(str)
    df[col_importe] = df[col_importe].str.replace(r'[^\d\.,\-]', '', regex=True)
    df[col_importe] = df[col_importe].str.replace('.', '', regex=False)
    df[col_importe] = df[col_importe].str.replace(',', '.', regex=False)
    df[col_importe] = pd.to_numeric(df[col_importe], errors='coerce')
    
    # Filtrar gastos (negativos)
    df_gastos = df[df[col_importe] < 0].copy()
    
    # Convertir los importes a positivo para los reportes
    df_gastos[col_importe] = df_gastos[col_importe].abs()
    
    # Aplicar la súper limpieza de texto al concepto bancario
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].apply(normalizar_texto)
    
    return df_gastos

def clasificar_gastos(df, reglas):
    def asignar_categoria(concepto):
        for categoria, lista_palabras in reglas.items():
            for palabra_clave in lista_palabras:
                palabra_limpia = normalizar_texto(palabra_clave)
                
                # 1. Dividimos tu palabra clave en palabras sueltas (Ej: ["JOSE", "MARTINEZ"])
                palabras_de_la_regla = palabra_limpia.split()
                
                # 2. Comprobamos si TODAS las palabras de tu regla están en el concepto del banco
                # Usamos 'all()' para asegurar que no falta ni una.
                if all(palabra in concepto for palabra in palabras_de_la_regla):
                    return categoria
                    
        return "SIN CLASIFICAR"
    
    # 1. Asigna la categoría detallada
    df['Categoria_Detalle'] = df['Concepto_limpio'].apply(asignar_categoria)
    
    # 2. Extrae la Categoría Padre cortando por el guion
    df['Categoria_Global'] = df['Categoria_Detalle'].str.split(' - ').str[0].str.strip()
    
    return df

def ejecutar_pipeline():
    print("🚀 Iniciando categorización de gastos...")
    
    reglas = cargar_reglas()
    df_gastos = limpiar_datos(ARCHIVO_REAL)
    df_clasificado = clasificar_gastos(df_gastos, reglas)
    
    # Aislar lo que no se ha podido clasificar
    df_sin_clasificar = df_clasificado[df_clasificado['Categoria_Detalle'] == "SIN CLASIFICAR"]
    
    # Agrupar los no clasificados para ver cuáles se repiten más
    pendientes = df_sin_clasificar.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    pendientes = pendientes.sort_values(by='Frecuencia', ascending=False)
    
    # Crear la tabla de resumen de gastos totales agrupados por categoría padre
    resumen_totales = df_clasificado.groupby('Categoria_Global')['Importe'].sum().reset_index()
    resumen_totales = resumen_totales.sort_values(by='Importe', ascending=False)
    
    # --- NUEVO: CÁLCULO DE LA SUMA TOTAL ---
    # Calculamos la suma de la columna Importe
    suma_total = resumen_totales['Importe'].sum()
    # Creamos una nueva fila con la etiqueta y el valor
    fila_total = pd.DataFrame([{'Categoria_Global': 'TOTAL GASTOS', 'Importe': suma_total}])
    # La enganchamos al final de la tabla usando pd.concat
    resumen_totales = pd.concat([resumen_totales, fila_total], ignore_index=True)
    # ---------------------------------------
    
    # Exportar los 3 archivos a Excel
    df_clasificado.to_excel(SALIDA_REPORTE, index=False)
    pendientes.to_excel(SALIDA_PENDIENTES, index=False)
    resumen_totales.to_excel(SALIDA_RESUMEN, index=False)
    
    # Mostrar resultados en consola
    print("\n📊 RESUMEN DE EJECUCIÓN:")
    print(f"Total de movimientos analizados: {len(df_clasificado)}")
    print(f"Movimientos clasificados con éxito: {len(df_clasificado) - len(df_sin_clasificar)}")
    print(f"Movimientos SIN CLASIFICAR: {len(df_sin_clasificar)}")
    print(f"💸 Gasto total registrado: {suma_total:,.2f} €")
    print("\nArchivos generados en data/output/:")
    print("1. gastos_clasificados.xlsx (El reporte completo detallado)")
    print("2. pendientes_clasificar.xlsx (Tu lista de tareas para añadir al JSON)")
    print("3. resumen_totales.xlsx (La suma de cuánto has gastado en cada partida + TOTAL)")

if __name__ == "__main__":
    ejecutar_pipeline()