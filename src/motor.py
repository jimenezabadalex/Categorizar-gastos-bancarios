import pandas as pd
import unicodedata

def normalizar_texto(texto):
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto_limpio = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto_limpio

def limpiar_datos(ruta, fecha_inicio=None, fecha_fin=None):
    # Leemos el Excel igual que siempre
    df = pd.read_excel(ruta, skiprows=3)
    
    # --- NUEVO: FILTRADO DE FECHAS ---
    # Buscamos la columna que contenga la palabra "FECHA" (por si el banco la llama "Fecha valor" o "Fecha de operación")
    col_fecha = next((col for col in df.columns if 'FECHA' in col.upper()), None)
    
    if col_fecha:
        # Convertimos la columna a un formato de tiempo real (día/mes/año)
        df[col_fecha] = pd.to_datetime(df[col_fecha], dayfirst=True, errors='coerce')
        
        # Recortamos el Excel si el usuario ha dado una fecha de inicio
        if fecha_inicio:
            fecha_inicio_dt = pd.to_datetime(fecha_inicio, dayfirst=True)
            df = df[df[col_fecha] >= fecha_inicio_dt]
            
        # Recortamos el Excel si el usuario ha dado una fecha de fin
        if fecha_fin:
            # Añadimos 23:59:59 para incluir todas las operaciones de ese último día
            fecha_fin_dt = pd.to_datetime(f"{fecha_fin} 23:59:59", dayfirst=True)
            df = df[df[col_fecha] <= fecha_fin_dt]
    # ---------------------------------
    
    # Si después de filtrar no hay datos, devolvemos tablas vacías
    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), 0.0

    col_importe = "Importe"
    col_concept = "Concepto"
    
    # 1. Limpieza matemática del importe
    df[col_importe] = df[col_importe].astype(str)
    df[col_importe] = df[col_importe].str.replace(r'[^\d\.,\-]', '', regex=True)
    df[col_importe] = df[col_importe].str.replace('.', '', regex=False)
    df[col_importe] = df[col_importe].str.replace(',', '.', regex=False)
    df[col_importe] = pd.to_numeric(df[col_importe], errors='coerce')
    
    # --- CÁLCULO INTELIGENTE DEL SALDO INICIAL ---
    saldo_inicial = 0.0
    col_saldo = next((col for col in df.columns if col.upper() == 'SALDO'), None)
    
    if col_saldo:
        df[col_saldo] = df[col_saldo].astype(str)
        df[col_saldo] = df[col_saldo].str.replace(r'[^\d\.,\-]', '', regex=True)
        df[col_saldo] = df[col_saldo].str.replace('.', '', regex=False)
        df[col_saldo] = df[col_saldo].str.replace(',', '.', regex=False)
        df[col_saldo] = pd.to_numeric(df[col_saldo], errors='coerce')
        
        saldo_antiguo = df.iloc[-1][col_saldo]
        importe_antiguo = df.iloc[-1][col_importe]
        saldo_inicial = saldo_antiguo - importe_antiguo
    
    # 2. Rutas de gastos e ingresos
    df_gastos = df[df[col_importe] < 0].copy()
    df_gastos[col_importe] = df_gastos[col_importe].abs() 
    df_gastos['Concepto_limpio'] = df_gastos[col_concept].apply(normalizar_texto)
    
    df_ingresos = df[df[col_importe] > 0].copy()
    df_ingresos['Concepto_limpio'] = df_ingresos[col_concept].apply(normalizar_texto)
    
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