import pandas as pd
import json
from config import DIR_INGRESOS, BASE_DIR

def crear_reglas_automaticas():
    print("🤖 Generando reglas de ingresos automáticamente...")
    
    # Leemos el archivo de conceptos únicos que generamos antes
    ruta_conceptos = DIR_INGRESOS / "conceptos_unicos_ingresos.xlsx"
    df = pd.read_excel(ruta_conceptos)
    
    # Preparamos la estructura base del JSON
    reglas = {
        "Impuestos - Devoluciones Hacienda": [],
        "Ingresos - Particulares": []
    }
    
    # Palabras clave de Hacienda
    kw_hacienda = ["AEAT", "AGENCIA TRIBUTARIA", "TESORO PUBLICO", "HACIENDA"]
    
    # Palabras clave de Empresas (con espacios para evitar falsos positivos)
    kw_empresas = [
        " SL ", " S.L ", " S.L.", " SL.", 
        " SA ", " S.A ", " S.A.", " SA.", 
        " SLU ", " S.L.U", " S.L.U.",
        " SAU ", " S.A.U", " S.A.U.",
        " SU ", " S.U ", " S.U.",
        " SLP ", " S.L.P", 
        " SOCIEDAD LIMITADA", " SOCIEDAD ANONIMA", 
        " S.COOP", " S COOP", " COOPERATIVA"
    ]
    
    for concepto in df['Concepto']:
        c = str(concepto)
        
        # Le añadimos un espacio al principio y al final a la frase del banco. 
        # Así, si pone "TRANSFERENCIA EMPRESA SL", la búsqueda de " SL " encajará perfectamente.
        c_padded = f" {c} " 
        
        # 1. ¿Es de Hacienda?
        if any(kw in c_padded for kw in kw_hacienda):
            reglas["Impuestos - Devoluciones Hacienda"].append(c)
            continue
            
        # 2. ¿Es Empresa?
        es_empresa = False
        for kw in kw_empresas:
            if kw in c_padded:
                es_empresa = True
                break
                
        if es_empresa:
            # Creamos una categoría única en el JSON dedicada SOLO a esta empresa
            nombre_categoria = f"Empresa - {c}"
            reglas[nombre_categoria] = [c]
            
        else:
            # 3. Si no es Hacienda ni tiene sufijo de empresa, va a Particulares
            reglas["Ingresos - Particulares"].append(c)
            
    # Guardar el resultado en el archivo JSON definitivo
    ruta_json = BASE_DIR / "config" / "reglas_ingresos.json"
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(reglas, f, indent=4, ensure_ascii=False)
        
    print(f"✅ ¡Éxito! Archivo creado en: {ruta_json}")
    
    # Pequeño resumen estadístico
    num_empresas = len([k for k in reglas.keys() if k.startswith('Empresa -')])
    num_particulares = len(reglas["Ingresos - Particulares"])
    print(f"🏢 Empresas independientes detectadas: {num_empresas}")
    print(f"👤 Particulares agrupados: {num_particulares}")

if __name__ == "__main__":
    crear_reglas_automaticas()