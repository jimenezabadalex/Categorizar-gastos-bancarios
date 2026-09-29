# 📊 Analizador Financiero Automatizado (Bank Analytics)

## 💡 Visión y Objetivos del Proyecto
Este proyecto nació con el propósito de refinar y construir una herramienta de análisis financiero basada en Python que fuera **totalmente automatizada, modular y fácil de usar**. El objetivo principal es minimizar al máximo la necesidad de hacer ajustes manuales en el código mes a mes, garantizando al mismo tiempo una **alta precisión matemática** en el cuadre de las cuentas bancarias.

## 🎯 ¿Qué es este proyecto y para qué sirve?
Este ecosistema de scripts toma los extractos bancarios en crudo (archivos Excel) y los transforma en informes clasificados, calculando con exactitud el flujo de caja y los saldos reales.

El sistema resuelve un problema común en la contabilidad automatizada: **la diferencia entre gastos e ingresos**. 
- Para los **gastos**, prioriza la precisión total permitiendo al usuario definir reglas estrictas mediante palabras clave (evitando categorías basura).
- Para los **ingresos**, utiliza un sistema de auto-generación que detecta empresas y particulares automáticamente.

## ⚠️ Nota Importante sobre Adaptabilidad (Disclaimer)
Este sistema ha sido diseñado y optimizado como una solución a medida para un caso de uso personal, adaptado al formato exacto de exportación Excel de una entidad bancaria específica. **No es un software *plug-and-play* universal para cualquier negocio o banco.**

Si otro usuario o empresa desea implementar este sistema, deberá adaptar el código a su contexto. Principalmente:
1. **El Motor de Lectura (`src/motor.py`):** La función `limpiar_datos()` asume que el Excel tiene una estructura concreta (ej. ignorar las 3 primeras filas con `skiprows=3`) y busca columnas específicas ("Importe", "Concepto", "Saldo"). Deberás mapear estos valores al formato de tu propio banco.
2. **La Lógica de Negocio:** El sistema asume que los ingresos se dividen principalmente en "Empresas" y "Particulares", y que los gastos se controlan al milímetro de forma manual. Una empresa con un modelo de facturación diferente (ej. e-commerce masivo) requeriría modificar el enfoque de las reglas.

El proyecto está diseñado de forma **altamente modular** precisamente para facilitar esta adaptación: puedes reescribir por completo cómo se lee el Excel en `motor.py` sin que el resto del programa deje de funcionar.

---

## ✨ Características Principales
* **Cálculo de Saldo Inteligente (Ingeniería Inversa):** El programa viaja a la fecha más antigua del extracto, lee el saldo y el importe de esa operación, y despeja la ecuación matemática para saber exactamente con cuánto dinero empezaste el periodo.
* **Interfaz de Terminal Interactiva:** Menú dinámico que detecta automáticamente los archivos Excel disponibles en la carpeta de entrada.
* **Filtros Temporales:** Permite analizar el histórico completo o recortar el análisis entre dos fechas específicas, recalculando el saldo inicial de forma dinámica.
* **Modular y Escalable:** Las reglas de negocio (diccionarios JSON) están separadas de la lógica del código (Python).

---

## 🏗️ Arquitectura y Flujo de Trabajo

### 1. El Núcleo de Análisis (Uso diario)
El análisis principal se ejecuta con `main.py`. Este archivo coordina el proceso:
1. Lee la carpeta `data/input/` y te pide elegir un Excel.
2. Te permite filtrar por fechas de inicio y fin.
3. El `motor.py` limpia los datos, corrige formatos numéricos, calcula el saldo inicial y separa gastos de ingresos.
4. Genera reportes detallados en `data/output/` divididos en Gastos e Ingresos (Clasificados, Resúmenes Totales y Pendientes de clasificar).

### 2. Herramientas Auxiliares y Mantenimiento
Para que el sistema sea fácil de mantener a lo largo de los años, el proyecto incluye herramientas extra (`src/`):

* 🔍 **`exploration.py` (Explorador de Gastos):** Escanea los gastos "SIN CLASIFICAR", extrae los conceptos únicos y te ayuda a identificar rápidamente qué nuevas palabras clave debes añadir a tus reglas manuales.
* 🔍 **`explorar_ingresos.py` (Explorador de Ingresos):** Realiza la misma labor de exploración, pero enfocado en las entradas de dinero.
* 🤖 **`generar_reglas_ingresos.py` (Creador de Reglas Automático):** Coge los resultados del explorador de ingresos y genera automáticamente el archivo de reglas, clasificando el dinero entrante en "Empresas" y "Particulares - Varios".
* 🩺 **`diagnostico.py` (Auditor Financiero):** Verifica la integridad estructural del Excel del banco buscando filas ignoradas y comprueba que el flujo calculado por Python cuadra al céntimo con el banco.

---

## 📂 Estructura de Directorios

```text
analitics-bank/
├── data/
│   ├── input/               # Directorio para los extractos bancarios en bruto (.xlsx)
│   └── output/              # Reportes generados automáticamente
│       ├── gastos/          
│       └── ingresos/        
├── config/                  
│   ├── reglas.json          # Diccionario manual de categorías de gastos
│   └── reglas_ingresos.json # Diccionario auto-generado de categorías de ingresos
├── src/                     
│   ├── main.py              # Orquestador e interfaz principal
│   ├── motor.py             # Lógica de limpieza, matemáticas y clasificación
│   ├── config.py            # Gestor de rutas del sistema
│   ├── exploration.py       # Herramienta de extracción de conceptos (Gastos)
│   ├── explorar_ingresos.py # Herramienta de extracción de conceptos (Ingresos)
│   ├── generar_reglas_...py # Generador automático de JSON para ingresos
│   └── diagnostico.py       # Auditor de integridad de datos
└── .gitignore               # Protección de datos confidenciales locales
```

## 🛠️ Requisitos Técnicos

*   Python 3.8 o superior.
*   Librerías requeridas: `pandas`, `openpyxl`.

Puedes instalar las dependencias con:
```bash
pip install pandas openpyxl
```

## 💻 Instrucciones de Uso

1. Coloca tu extracto bancario en formato Excel (`.xlsx`) dentro de la carpeta `data/input/`.
2. Ejecuta el pipeline principal desde la raíz del proyecto:
   ```bash
   python src/main.py
   ```
3. Elige el archivo a analizar en el menú interactivo.
4. (Opcional) Introduce las fechas de inicio y fin para acotar el análisis.
5. Revisa los resultados por consola y consulta los reportes detallados en la carpeta `data/output/`.
