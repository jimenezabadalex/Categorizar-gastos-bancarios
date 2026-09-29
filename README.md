# 📊 Auditor Financiero Automatizado

Una herramienta de análisis de datos desarrollada en Python para automatizar la contabilidad personal y profesional. Este script procesa extractos bancarios en bruto (formato Excel), limpia los datos, clasifica los movimientos y genera reportes financieros detallados con los saldos reales y flujos de caja.

## 🚀 Características Principales

*   **Menú Interactivo (CLI):** Detección automática de archivos en la carpeta de entrada y selección mediante menú en la terminal.
*   **Análisis Temporal Dinámico:** Capacidad para filtrar el análisis por rango de fechas (Inicio - Fin).
*   **Cálculo Inteligente de Saldo Inicial:** Utiliza ingeniería inversa matemática sobre la última fila del extracto para calcular el saldo de inicio exacto, permitiendo cuadrar los resultados al céntimo con la entidad bancaria, sin importar los filtros de fecha aplicados.
*   **Motor de Categorización Híbrido:** 
    *   *Ingresos:* Categorización 100% automática basada en sufijos y nombres de empresas/particulares.
    *   *Gastos:* Clasificación basada en reglas estrictas (diccionarios JSON) para evitar el "ruido" de categorías inútiles y mantener una ontología de gastos limpia.
*   **Generación de Reportes:** Exporta los resultados clasificados, un resumen de totales y un listado de movimientos "pendientes de clasificar" para facilitar el entrenamiento del modelo.

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura modular para separar la configuración, los datos y la lógica de negocio:

```text
analitics-bank/
├── data/                    # (Ignorado en Git por privacidad)
│   ├── input/               # Depositar aquí los archivos .xlsx del banco
│   └── output/              # Reportes generados (separados en /gastos e /ingresos)
├── config/                  # Reglas de negocio (Ignorado en Git)
│   ├── reglas.json          # Diccionario de categorización de gastos
│   └── reglas_ingresos.json # Diccionario de categorización de ingresos
├── src/                     # Código fuente
│   ├── config.py            # Gestor de rutas
│   ├── motor.py             # Limpieza de datos (Pandas) y lógica matemática
│   ├── main.py              # Interfaz CLI y pipeline de ejecución
│   └── diagnostico.py       # Herramienta de auditoría para detectar errores de formato
└── .gitignore               # Protección de datos confidenciales y caché
```

## 🛠️ Requisitos Técnicos

*   Python 3.8 o superior.
*   Librerías requeridas: `pandas`, `openpyxl`.

Puedes instalar las dependencias con:
```bash
pip install pandas openpyxl
```

## 💻 Instrucciones de Uso

1.  Coloca tu extracto bancario en formato Excel (`.xlsx`) dentro de la carpeta `data/input/`.
2.  Ejecuta el pipeline principal desde la raíz del proyecto:
    ```bash
    python src/main.py
    ```
3.  Elige el archivo a analizar en el menú interactivo.
4.  (Opcional) Introduce las fechas de inicio y fin para acotar el análisis.
5.  Revisa los resultados por consola y consulta los reportes detallados en la carpeta `data/output/`.

## 🔮 Próximos Pasos (Roadmap)
*   [ ] Implementación de interfaz gráfica web mediante **Streamlit**.
*   [ ] Generación de gráficos y visualizaciones interactivas.
*   [ ] Soporte multi-cuenta bancaria.