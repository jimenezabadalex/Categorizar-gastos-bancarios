import pandas as pd
from pathlib import Path

BASE_DIR =Path(__file__).parent.parent

#Apunto a la carpeta segun input

ARCHIVO_REAL= BASE_DIR / "data" / "input" / "2026.xlsx"

SALIDA_CONCEPTOS = BASE_DIR / "data" / "output" / "conceptos_unicos.xlsx"

def extraer_conceptos_unicos(ruta):

    # 1. Leo archivo, ajusta si hay filas basura arriba

    df = pd.read_excel(ruta, skiprows=3)

    # --- MODO DIAGNÓSTICO ---
    print("\n🔍 DIAGNÓSTICO DE COLUMNAS:")
    print("Pandas ha detectado estas columnas en tu archivo:")
    print(df.columns.tolist())
    print("-" * 30)
    # ------------------------

    col_importe = "Importe"
    col_concept = "Concepto"

   # --- Limpieza de la columna Importe ---
    df[col_importe] = df[col_importe].astype(str)
    
    # 2. MODO BLINDADO: Borramos TODO lo que no sea dígito (\d), punto (\.), coma (,) o menos (\-)
    df[col_importe] = df[col_importe].str.replace(r'[^\d\.,\-]', '', regex=True)
    
    # 3. Quitamos los puntos de los miles (12.732,17 -> 12732,17)
    df[col_importe] = df[col_importe].str.replace('.', '', regex=False)
    
    # 4. Cambiamos la coma decimal por el punto matemático (12732,17 -> 12732.17)
    df[col_importe] = df[col_importe].str.replace(',', '.', regex=False)
    
    # 5. Convertimos a número matemático para poder filtrar < 0
    df[col_importe] = pd.to_numeric(df[col_importe], errors='coerce')
    # ---------------------------------------------

   
    # 2. Filtrar gastos
    df_gastos = df[df[col_importe] < 0].copy()

    # 3. Limpiar gastos
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].astype(str).str.upper().str.strip()


    # 4. Extraer conceptos únicos, contar veces que se repiten y ordenar segun frecuencia

    conceptos_agrupados = df_gastos.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    conceptos_agrupados = conceptos_agrupados.sort_values(by= 'Frecuencia',ascending=False)

    # 5. Exportar para revisión 

    conceptos_agrupados.to_excel(SALIDA_CONCEPTOS,  index= False)
    print(f"Extraidos {len(conceptos_agrupados)} conceptos únicos.")
    print(f"Revisar archivo en: {SALIDA_CONCEPTOS}")


if __name__ == "__main__":
    extraer_conceptos_unicos(ARCHIVO_REAL)