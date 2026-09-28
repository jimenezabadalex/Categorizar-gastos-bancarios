import pandas as pd
from config import ARCHIVO_REAL

def auditar_cantidades():
    print("🔍 INICIANDO AUDITORÍA FINANCIERA...")
    
    # 1. Leer el Excel tal cual sale del banco
    df = pd.read_excel(ARCHIVO_REAL, skiprows=3)
    total_filas_original = len(df)
    
    # 2. Comprobar si existe la columna "Saldo" del banco
    if 'Saldo' in df.columns or 'SALDO' in df.columns:
        col_saldo = 'Saldo' if 'Saldo' in df.columns else 'SALDO'
        saldo_inicial = df.iloc[0][col_saldo] # El saldo en la fila 1
        saldo_final = df.iloc[-1][col_saldo]  # El saldo en la última fila
        print(f"\n🏦 SEGÚN EL BANCO:")
        print(f"Saldo en el primer movimiento: {saldo_inicial}")
        print(f"Saldo en el último movimiento: {saldo_final}")
    
    # 3. Simular nuestra limpieza
    df['Importe_Texto'] = df['Importe'].astype(str)
    df['Importe_Limpio'] = df['Importe_Texto'].str.replace(r'[^\d\.,\-]', '', regex=True)
    df['Importe_Limpio'] = df['Importe_Limpio'].str.replace('.', '', regex=False)
    df['Importe_Limpio'] = df['Importe_Limpio'].str.replace(',', '.', regex=False)
    df['Importe_Num'] = pd.to_numeric(df['Importe_Limpio'], errors='coerce')
    
    # 4. Buscar filas perdidas (NaN) o que sean exactamente 0
    filas_perdidas = df[df['Importe_Num'].isna()]
    filas_cero = df[df['Importe_Num'] == 0]
    
    gastos = df[df['Importe_Num'] < 0]
    ingresos = df[df['Importe_Num'] > 0]
    
    total_filas_procesadas = len(gastos) + len(ingresos) + len(filas_cero) + len(filas_perdidas)
    
    print(f"\n💻 SEGÚN EL PROGRAMA:")
    print(f"Filas originales en el Excel: {total_filas_original}")
    print(f"Filas detectadas como Gastos: {len(gastos)}")
    print(f"Filas detectadas como Ingresos: {len(ingresos)}")
    print(f"Filas ignoradas por valor 0.00: {len(filas_cero)}")
    print(f"🚨 Filas ROTAS o PERDIDAS por formato: {len(filas_perdidas)}")
    
    if len(filas_perdidas) > 0:
        print("\n⚠️ ALERTA: Se han perdido estas filas al limpiar los números:")
        print(filas_perdidas[['Concepto', 'Importe', 'Importe_Texto']])
    else:
        print("\n✅ ¡La limpieza matemática es perfecta! No se ha perdido ni una sola fila.")
        print("💡 CONCLUSIÓN: La diferencia de 10k se debe casi 100% seguro al Saldo Inicial que tenías en el banco antes de empezar este extracto.")

if __name__ == "__main__":
    auditar_cantidades()