import pandas as pd

from config import (
    ARCHIVO_REAL, NOMBRE_EXTRACTO, SALIDA_REPORTE, 
    SALIDA_PENDIENTES, SALIDA_RESUMEN, SALIDA_INGRESOS, cargar_reglas
)
from motor import limpiar_datos, clasificar_gastos

def ejecutar_pipeline():
    print("🚀 Iniciando categorización de cuenta bancaria...")
    
    reglas = cargar_reglas()
    df_gastos, df_ingresos = limpiar_datos(ARCHIVO_REAL)
    
    # --- PROCESAMIENTO DE GASTOS ---
    df_clasificado = clasificar_gastos(df_gastos, reglas)
    
    df_sin_clasificar = df_clasificado[df_clasificado['Categoria_Detalle'] == "SIN CLASIFICAR"]
    pendientes = df_sin_clasificar.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    pendientes = pendientes.sort_values(by='Frecuencia', ascending=False)
    
    resumen_totales = df_clasificado.groupby('Categoria_Global')['Importe'].sum().reset_index()
    resumen_totales = resumen_totales.sort_values(by='Importe', ascending=False)
    
    suma_gastos = resumen_totales['Importe'].sum()
    fila_total = pd.DataFrame([{'Categoria_Global': 'TOTAL GASTOS', 'Importe': suma_gastos}])
    resumen_totales = pd.concat([resumen_totales, fila_total], ignore_index=True)
    
    # --- PROCESAMIENTO DE INGRESOS ---
    df_ingresos = df_ingresos.sort_values(by='Importe', ascending=False)
    suma_ingresos = df_ingresos['Importe'].sum()
    
    # --- EXPORTAR ARCHIVOS ---
    df_clasificado.to_excel(SALIDA_REPORTE, index=False)
    pendientes.to_excel(SALIDA_PENDIENTES, index=False)
    resumen_totales.to_excel(SALIDA_RESUMEN, index=False)
    df_ingresos.to_excel(SALIDA_INGRESOS, index=False)
    
    # --- MOSTRAR RESULTADOS EN CONSOLA ---
    print("\n📊 RESUMEN DE EJECUCIÓN:")
    print(f"Total de movimientos de GASTO analizados: {len(df_clasificado)}")
    print(f"Gastos SIN CLASIFICAR: {len(df_sin_clasificar)}")
    print("-" * 30)
    print(f"💸 GASTO TOTAL: {suma_gastos:,.2f} €")
    print(f"💰 INGRESO TOTAL: {suma_ingresos:,.2f} €")
    print("-" * 30)
    print(f"📈 SALDO DEL PERIODO: {(suma_ingresos - suma_gastos):,.2f} €")
    
    # --- NUEVO: Textos de consola actualizados ---
    print("\nArchivos generados con éxito en data/output/:")
    print("📁 En la carpeta /gastos/:")
    print(f"  ├─ gastos_clasificados_{NOMBRE_EXTRACTO}.xlsx")
    print(f"  ├─ pendientes_clasificar_{NOMBRE_EXTRACTO}.xlsx")
    print(f"  └─ resumen_totales_{NOMBRE_EXTRACTO}.xlsx")
    print("📁 En la carpeta /ingresos/:")
    print(f"  └─ ingresos_{NOMBRE_EXTRACTO}.xlsx")

if __name__ == "__main__":
    ejecutar_pipeline()