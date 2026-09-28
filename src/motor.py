import pandas as pd
import unicodedata

def normalizar_texto(texto):
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto_limpio = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto_limpio

def limpiar_datos(ruta):
    df = pd.read_excel(ruta, skiprows=3)
    
    col_importe = "Importe"
    col_concept = "Concepto"
    
    # 1. Limpieza matemática del importe
    df[col_importe] = df[col_importe].astype(str)
    df[col_importe] = df[col_importe].str.replace(r'[^\d\.,\-]', '', regex=True)
    df[col_importe] = df[col_importe].str.replace('.', '', regex=False)
    df[col_importe] = df[col_importe].str.replace(',', '.', regex=False)
    df[col_importe] = pd.to_numeric(df[col_importe], errors='coerce')
    
    # --- NUEVO: CÁLCULO INTELIGENTE DEL SALDO INICIAL ---
    saldo_inicial = 0.0
    # Buscamos si existe una columna que se llame 'Saldo' (en mayúsculas o minúsculas)
    col_saldo = next((col for col in df.columns if col.upper() == 'SALDO'), None)
    
    if col_saldo:
        # Limpiamos la columna Saldo igual que limpiamos los importes
        df[col_saldo] = df[col_saldo].astype(str)
        df[col_saldo] = df[col_saldo].str.replace(r'[^\d\.,\-]', '', regex=True)
        df[col_saldo] = df[col_saldo].str.replace('.', '', regex=False)
        df[col_saldo] = df[col_saldo].str.replace(',', '.', regex=False)
        df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce')
        
        # Aplicamos la ecuación en la última fila (iloc[-1] es la fila más antigua)
        saldo_antiguo = df.iloc[-1][col_saldo]
        importe_antiguo = df.iloc[-1][col_importe]
        
        # Ecuación: Saldo Inicial = Saldo - Importe
        saldo_inicial = saldo_antiguo - importe_antiguo
    # ----------------------------------------------------
    
    # 2. Rutas de gastos e ingresos
    df_gastos = df[df[col_importe] < 0].copy()
    df_gastos[col_importe] = df_gastos[col_importe].abs() 
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].apply(normalizar_texto)
    
    df_ingresos = df[df[col_importe] > 0].copy()
    df_ingresos['Concepto_limpio'] = df_ingresos[col_concept].apply(normalizar_texto)
    
    # IMPORTANTE: Ahora devolvemos 3 cosas (añadimos el saldo_inicial)
    return df_gastos, df_ingresos, saldo_inicial

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