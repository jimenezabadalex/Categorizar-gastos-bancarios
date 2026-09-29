import pandas as pd
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Definimos las rutas
BASE_DIR = Path(__file__).parent.parent
DIR_INPUT = BASE_DIR / "data" / "input"
DIR_CONFIG = BASE_DIR / "config"

# Aseguramos que existan las carpetas
DIR_INPUT.mkdir(parents=True, exist_ok=True)
DIR_CONFIG.mkdir(parents=True, exist_ok=True)

def formato_banco(numero):
    """Convierte un float (1500.5) al formato de texto del banco ('1.500,50')"""
    texto = f"{numero:,.2f}"
    # Cambiamos las comas de miles por puntos y el punto decimal por coma
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")

def generar_excel_falso():
    ruta_excel = DIR_INPUT / "extracto_demo.xlsx"
    random.seed(42)  # Para que genere siempre los mismos datos aleatorios
    
    conceptos_gastos = [
        ("COMPRA MERCADONA", -30.0, -110.0),
        ("COMPRA CARREFOUR", -20.0, -80.0),
        ("RECIBO IBERDROLA", -45.0, -70.0),
        ("RECIBO ENDESA", -40.0, -60.0),
        ("AMAZON PRIME", -4.99, -4.99),
        ("NETFLIX", -12.99, -12.99),
        ("RESTAURANTE EL PINO", -20.0, -50.0),   # Intencionadamente fuera del JSON
        ("GASOLINERA REPSOL", -40.0, -70.0),     # Intencionadamente fuera del JSON
        ("BIZUM CENA", -15.0, -30.0)
    ]
    
    fecha_actual = datetime(2025, 10, 1)
    saldo_actual = 1850.00
    filas = []
    
    # Generamos 60 transacciones
    for i in range(60):
        # Avanzamos entre 1 y 3 días de forma aleatoria
        fecha_actual += timedelta(days=random.randint(1, 3))
        
        # Cada ~15 transacciones, metemos una nómina
        if i > 0 and i % 15 == 0:
            concepto = "NOMINA EMPRESA TECH S.L."
            importe = 1850.00
        else:
            compra = random.choice(conceptos_gastos)
            concepto = compra[0]
            # Si el precio es fijo (ej. Netflix), usamos ese. Si no, calculamos uno aleatorio
            if compra[1] == compra[2]:
                importe = compra[1]
            else:
                importe = round(random.uniform(compra[1], compra[2]), 2)
        
        # El saldo se actualiza matemáticamente
        saldo_actual += importe
        
        filas.append({
            'Fecha': fecha_actual.strftime("%d/%m/%Y"),
            'Concepto': concepto,
            'Importe': formato_banco(importe),
            'Saldo': formato_banco(saldo_actual)
        })
        
    # Los bancos muestran siempre la operación más reciente arriba del todo
    filas.reverse()
    
    df = pd.DataFrame(filas)
    
    with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, startrow=3)
        worksheet = writer.sheets['Sheet1']
        worksheet.cell(row=1, column=1, value="BANCO EJEMPLO - MOVIMIENTOS DE CUENTA")
        worksheet.cell(row=2, column=1, value="Titular: Usuario Demo")
        worksheet.cell(row=3, column=1, value="Cuenta: ES91 1234 5678 9012 3456 7890")
        
    print(f"✅ Excel de prueba creado con {len(filas)} movimientos en: {ruta_excel}")

def generar_json_ejemplos():
    ruta_reglas = DIR_CONFIG / "reglas.json.example"
    ruta_ingresos = DIR_CONFIG / "reglas_ingresos.json.example"
    
    # Reglas limitadas para que algunos gastos queden "SIN CLASIFICAR" a propósito
    reglas_gastos = {
        "Suministros - Hogar": ["IBERDROLA", "ENDESA"],
        "Alimentacion - Supermercado": ["MERCADONA", "CARREFOUR"],
        "Ocio - Suscripciones": ["AMAZON PRIME", "NETFLIX"]
    }
    
    reglas_ingresos = {
        "Ingreso - Nomina": ["NOMINA EMPRESA"],
        "Ingreso - Particulares": ["BIZUM CENA"]
    }
    
    with open(ruta_reglas, 'w', encoding='utf-8') as f:
        json.dump(reglas_gastos, f, indent=4, ensure_ascii=False)
        
    with open(ruta_ingresos, 'w', encoding='utf-8') as f:
        json.dump(reglas_ingresos, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Archivos JSON de ejemplo actualizados en: {DIR_CONFIG}")

if __name__ == "__main__":
    print("🛠️ Generando entorno de pruebas avanzado...")
    generar_excel_falso()
    generar_json_ejemplos()
    print("🚀 ¡Entorno de pruebas listo! Los reclutadores ya pueden probar el programa.")