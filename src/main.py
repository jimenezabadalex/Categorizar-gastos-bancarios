import pandas as pd

from config import (
    DIR_INPUT, DIR_GASTOS, DIR_INGRESOS, 
    cargar_reglas, cargar_reglas_ingresos
)
from motor import limpiar_datos, clasificar_movimientos

def seleccionar_archivo():
    # Buscamos todos los archivos .xlsx en la carpeta input
    archivos = list(DIR_INPUT.glob("*.xlsx"))
    
    if not archivos:
        print("❌ No se encontraron archivos Excel en la carpeta data/input/")
        return None
        
    print("\n📂 ARCHIVOS DISPONIBLES:")
    for i, archivo in enumerate(archivos):
        print(f"  [{i + 1}] {archivo.name}")
        
    while True:
        try:
            seleccion = int(input("\n👉 Elige el número del archivo a analizar: ")) - 1
            if 0 <= seleccion < len(archivos):
                return archivos[seleccion]
            else:
                print("⚠️ Número fuera de rango. Inténtalo de nuevo.")
        except ValueError:
            print("⚠️ Por favor, introduce un número válido.")

def ejecutar_pipeline():
    print("🚀 Bienvenido al Analizador Financiero")
    
    # 1. Menú de selección de archivo
    archivo_real = seleccionar_archivo()
    if not archivo_real:
        return
        
    nombre_extracto = archivo_real.stem
    print(f"\n✅ Archivo seleccionado: {archivo_real.name}")
    
    # 2. Fechas (dejamos la interfaz que ya teníamos)
    print("\nDeje en blanco y pulse ENTER para analizar todo el documento.")
    fecha_inicio = input("📅 Introduce fecha de INICIO (DD/MM/AAAA): ").strip()
    fecha_fin = input("📅 Introduce fecha de FIN (DD/MM/AAAA): ").strip()
    
    fecha_inicio = fecha_inicio if fecha_inicio else None
    fecha_fin = fecha_fin if fecha_fin else None
    
    if fecha_inicio or fecha_fin:
        print(f"\n⏳ Analizando periodo: {fecha_inicio or 'Inicio'} al {fecha_fin or 'Final'}...")
    else:
        print("\n⏳ Analizando todo el histórico completo...")

    # --- NUEVO: DETECCIÓN MODO DEMO ---
    es_demo = (archivo_real.name == "extracto_demo.xlsx")
    if es_demo:
        print("\n🧪 [MODO DEMO DETECTADO] Usando reglas de ejemplo para la clasificación...")
        
    reglas_gastos = cargar_reglas(es_demo)
    reglas_ingresos = cargar_reglas_ingresos(es_demo)
    # ----------------------------------
        

    
    # --- PASAMOS EL ARCHIVO ELEGIDO AL MOTOR ---
    df_gastos, df_ingresos, saldo_inicial = limpiar_datos(archivo_real, fecha_inicio, fecha_fin)
    
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
    
    # --- 3. EXPORTAR ARCHIVOS (Ahora con nombres dinámicos) ---
    salida_reporte = DIR_GASTOS / f"gastos_clasificados_{nombre_extracto}.xlsx"
    salida_pendientes = DIR_GASTOS / f"pendientes_clasificar_{nombre_extracto}.xlsx"
    salida_resumen = DIR_GASTOS / f"resumen_totales_{nombre_extracto}.xlsx"
    
    salida_reporte_ingresos = DIR_INGRESOS / f"ingresos_clasificados_{nombre_extracto}.xlsx"
    salida_pendientes_ingresos = DIR_INGRESOS / f"pendientes_clasificar_ingresos_{nombre_extracto}.xlsx"
    salida_resumen_ingresos = DIR_INGRESOS / f"resumen_totales_ingresos_{nombre_extracto}.xlsx"

    df_gastos_clasificado.to_excel(salida_reporte, index=False)
    pendientes_gastos.to_excel(salida_pendientes, index=False)
    resumen_gastos.to_excel(salida_resumen, index=False)
    
    df_ingresos_clasificado.to_excel(salida_reporte_ingresos, index=False)
    pendientes_ingresos.to_excel(salida_pendientes_ingresos, index=False)
    resumen_ingresos.to_excel(salida_resumen_ingresos, index=False)
    
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