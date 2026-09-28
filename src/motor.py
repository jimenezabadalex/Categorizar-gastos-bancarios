import pandas as pd
import unicodedata

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
    
    # --- 1. RUTA DE GASTOS (negativos) ---
    df_gastos = df[df[col_importe] < 0].copy()
    df_gastos[col_importe] = df_gastos[col_importe].abs() # Convertir a positivo para los reportes
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].apply(normalizar_texto)
    
    # --- 2. RUTA DE INGRESOS (positivos) ---
    df_ingresos = df[df[col_importe] > 0].copy()
    df_ingresos['Concepto_limpio'] = df_ingresos[col_concept].apply(normalizar_texto)
    
    # Devolvemos ambas tablas por separado
    return df_gastos, df_ingresos

# RENOMBRADO: Ahora sirve tanto para ingresos como para gastos
def clasificar_movimientos(df, reglas):
    def asignar_categoria(concepto):
        for categoria, lista_palabras in reglas.items():
            for palabra_clave in lista_palabras:
                palabra_limpia = normalizar_texto(palabra_clave)
                palabras_de_la_regla = palabra_limpia.split()
                
                if all(palabra in concepto for palabra in palabras_de_la_regla):
                    return categoria
        return "SIN CLASIFICAR"
    
    df['Categoria_Detalle'] = df['Concepto_limpio'].apply(asignar_categoria)
    df['Categoria_Global'] = df['Categoria_Detalle'].str.split(' - ').str[0].str.strip()
    
    return df