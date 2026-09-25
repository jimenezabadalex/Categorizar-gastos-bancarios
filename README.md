\# 📊 Categorización Automática de Gastos Bancarios 



> Herramienta automatizada en Python para limpiar, clasificar y consolidar movimientos bancarios corporativos, facilitando el cierre contable y el análisis financiero mensual.



\## 🎯 Contexto del Negocio

En el entorno actual de la empresa, los ingresos están completamente monitorizados mediante un software de facturación. Sin embargo, existía un punto ciego respecto al control de las salidas de caja. Este proyecto resuelve ese problema implementando un pipeline ETL (Extract, Transform, Load) en local. El sistema ingesta los extractos bancarios en formato Excel, aísla los gastos y les asigna categorías automáticamente mediante un motor de reglas basado en palabras clave.



\## 💡 Impacto

\* \*\*Eficiencia Operativa:\*\* Transforma un proceso manual de horas en una ejecución de segundos.

\* \*\*Visibilidad Financiera:\*\* Proporciona un desglose claro de los gastos (suministros, nóminas, servicios) para una mejor toma de decisiones.

\* \*\*Mejora Continua:\*\* El sistema aísla los movimientos "SIN CLASIFICAR", permitiendo actualizar fácilmente el diccionario de reglas mes a mes para rozar el 100% de precisión.



\## 🛠️ Stack Tecnológico

\* \*\*Lenguaje:\*\* Python 3.x

\* \*\*Manipulación y Análisis de Datos:\*\* `pandas`

\* \*\*Lectura/Escritura de Archivos:\*\* `openpyxl`



\## 📂 Arquitectura del Proyecto



```text

├── data/

│   ├── input/       # (Oculto en git) .xlsx originales descargados del banco

│   ├── output/      # (Oculto en git) Reportes categorizados y listos para análisis

│   ├── archive/     # (Oculto en git) Histórico de archivos ya procesados

│   └── sample/      # Dataset dummy (ficticio) para demostraciones del código

├── src/

│   ├── main.py            # Orquestador del pipeline

│   ├── limpieza.py        # Módulo de estandarización (fechas, strings, nulos)

│   └── categorizacion.py  # Motor de asignación de reglas cruzadas

├── config/

│   └── reglas.json        # Diccionario clave-valor para la categorización

├── .gitignore

├── requirements.txt

└── README.md

