import pandas as pd

# --- ESTO ES LO ÚNICO NUEVO QUE HE AÑADIDO ---
# Importamos las rutas y funciones desde nuestros nuevos archivos
from config import (
    ARCHIVO_REAL, NOMBRE_EXTRACTO, SALIDA_REPORTE, 
    SALIDA_PENDIENTES, SALIDA_RESUMEN, cargar_reglas
)
from motor import limpiar_datos, clasificar_gastos
# ---------------------------------------------

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
    
    # Cálculo de la suma total
    suma_total = resumen_totales['Importe'].sum()
    fila_total = pd.DataFrame([{'Categoria_Global': 'TOTAL GASTOS', 'Importe': suma_total}])
    resumen_totales = pd.concat([resumen_totales, fila_total], ignore_index=True)
    
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
    print(f"1. gastos_clasificados_{NOMBRE_EXTRACTO}.xlsx (El reporte completo detallado)")
    print(f"2. pendientes_clasificar_{NOMBRE_EXTRACTO}.xlsx (Tu lista de tareas)")
    print(f"3. resumen_totales_{NOMBRE_EXTRACTO}.xlsx (La suma por partidas + TOTAL)")

if __name__ == "__main__":
    ejecutar_pipeline()