import pandas as pd

from config import (
    ARCHIVO_REAL, NOMBRE_EXTRACTO, 
    SALIDA_REPORTE, SALIDA_PENDIENTES, SALIDA_RESUMEN, cargar_reglas,
    SALIDA_REPORTE_INGRESOS, SALIDA_PENDIENTES_INGRESOS, SALIDA_RESUMEN_INGRESOS, cargar_reglas_ingresos
)
from motor import limpiar_datos, clasificar_movimientos

def ejecutar_pipeline():
    print("🚀 Bienvenido al Analizador Financiero")
    print("Deje en blanco y pulse ENTER para analizar todo el documento.\n")
    
    # --- INTERFAZ DE USUARIO ---
    fecha_inicio = input("📅 Introduce fecha de INICIO (DD/MM/AAAA): ").strip()
    fecha_fin = input("📅 Introduce fecha de FIN (DD/MM/AAAA): ").strip()
    
    # Si están en blanco, las pasamos como None
    fecha_inicio = fecha_inicio if fecha_inicio else None
    fecha_fin = fecha_fin if fecha_fin else None
    
    if fecha_inicio or fecha_fin:
        print(f"\n⏳ Analizando periodo: {fecha_inicio or 'Inicio'} al {fecha_fin or 'Final'}...")
    else:
        print("\n⏳ Analizando todo el histórico completo...")
        
    reglas_gastos = cargar_reglas()
    reglas_ingresos = cargar_reglas_ingresos()
    
    # --- PASAMOS LAS FECHAS AL MOTOR ---
    df_gastos, df_ingresos, saldo_inicial = limpiar_datos(ARCHIVO_REAL, fecha_inicio, fecha_fin)
    
    # Evitar error si el usuario pone una fecha donde no hay movimientos
    if df_gastos.empty and df_ingresos.empty:
        print("\n❌ No hay movimientos en este rango de fechas. Operación cancelada.")
        return
    
    # --- 1. PROCESAMIENTO DE GASTOS ---
    df_gastos_clasificado = clasificar_movimientos(df_gastos, reglas_gastos)
    
    pend_gastos_df = df_gastos_clasificado[df_gastos_clasificado['Categoria_Detalle'] == "SIN CLASIFICAR"]
    pendientes_gastos = pend_gastos_df.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    pendientes_gastos = pendientes_gastos.sort_values(by='Frecuencia', ascending=False)
    
    resumen_gastos = df_gastos_clasificado.groupby('Categoria_Global')['Importe'].sum().reset_index()
    resumen_gastos = resumen_gastos.sort_values(by='Importe', ascending=False)
    
    suma_gastos = resumen_gastos['Importe'].sum()
    fila_total_g = pd.DataFrame([{'Categoria_Global': 'TOTAL GASTOS', 'Importe': suma_gastos}])
    resumen_gastos = pd.concat([resumen_gastos, fila_total_g], ignore_index=True)
    
    # --- 2. PROCESAMIENTO DE INGRESOS ---
    df_ingresos_clasificado = clasificar_movimientos(df_ingresos, reglas_ingresos)
    
    pend_ingresos_df = df_ingresos_clasificado[df_ingresos_clasificado['Categoria_Detalle'] == "SIN CLASIFICAR"]
    pendientes_ingresos = pend_ingresos_df.groupby('Concepto_limpio').size().reset_index(name='Frecuencia')
    pendientes_ingresos = pendientes_ingresos.sort_values(by='Frecuencia', ascending=False)
    
    resumen_ingresos = df_ingresos_clasificado.groupby('Categoria_Global')['Importe'].sum().reset_index()
    resumen_ingresos = resumen_ingresos.sort_values(by='Importe', ascending=False)
    
    suma_ingresos = resumen_ingresos['Importe'].sum()
    fila_total_i = pd.DataFrame([{'Categoria_Global': 'TOTAL INGRESOS', 'Importe': suma_ingresos}])
    resumen_ingresos = pd.concat([resumen_ingresos, fila_total_i], ignore_index=True)
    
    # --- 3. EXPORTAR ARCHIVOS ---
    df_gastos_clasificado.to_excel(SALIDA_REPORTE, index=False)
    pendientes_gastos.to_excel(SALIDA_PENDIENTES, index=False)
    resumen_gastos.to_excel(SALIDA_RESUMEN, index=False)
    
    df_ingresos_clasificado.to_excel(SALIDA_REPORTE_INGRESOS, index=False)
    pendientes_ingresos.to_excel(SALIDA_PENDIENTES_INGRESOS, index=False)
    resumen_ingresos.to_excel(SALIDA_RESUMEN_INGRESOS, index=False)
    
    # --- 4. MOSTRAR RESULTADOS EN CONSOLA ---
    flujo_periodo = suma_ingresos - suma_gastos
    saldo_final_banco = saldo_inicial + flujo_periodo
    
    print("\n📊 RESUMEN DE EJECUCIÓN:")
    print(f"Gastos SIN CLASIFICAR: {len(pend_gastos_df)} de {len(df_gastos_clasificado)}")
    print(f"Ingresos SIN CLASIFICAR: {len(pend_ingresos_df)} de {len(df_ingresos_clasificado)}")
    print("-" * 30)
    print(f"🏦 SALDO INICIAL AUTOMÁTICO: {saldo_inicial:,.2f} €")
    print(f"💰 INGRESOS TOTALES: +{suma_ingresos:,.2f} €")
    print(f"💸 GASTOS TOTALES: -{suma_gastos:,.2f} €")
    print(f"📈 FLUJO DEL PERIODO: {flujo_periodo:,.2f} €")
    print("-" * 30)
    print(f"✅ SALDO FINAL EN BANCO: {saldo_final_banco:,.2f} €")

if __name__ == "__main__":
    ejecutar_pipeline()