# 🏎️ F1 Data Pipeline: Analytics & Automation (2026)

Este proyecto implementa un pipeline automatizado de ingeniería de datos (ETL) para la extracción, procesamiento y carga de telemetría e información histórica de la **Fórmula 1 (Temporada 2026)**. La arquitectura integra el desarrollo local en Python con el almacenamiento en la nube de **Google Cloud Platform (GCP)** y la automatización mediante **GitHub Actions**.

## 📌 Arquitectura del Proyecto

El flujo de datos se divide en tres etapas principales controladas de forma automática:



1. **Extracción (Extract):** Descarga de calendarios, resultados y tiempos de vueltas directamente desde la API de la librería `fastf1`.
2. **Transformación (Transform):** Limpieza, estructuración y conversión de dataframes de Pandas a archivos comprimidos de alta eficiencia en formato `.parquet`.
3. **Carga (Load):** Conexión segura mediante la cuenta de servicio de Google Cloud para subir los archivos organizados bajo la estructura virtual *Hive-Style* (`year=2026/`).

---

## 📂 Estructura del Repositorio

```text
F1-Analysis/
├── .github/workflows/
│   └── extract.yml       # Orquestador automatizado de GitHub Actions
├── scripts/
│   ├── extract.py        # Script de extracción de API y conversión a Parquet
│   ├── load.py           # Script de transporte y particionamiento en GCS
│   └── utils.py          # Herramientas de soporte, entorno y cliente de Google
├── data/
│   ├── cache/            # Caché local de FastF1 (ignorado en Git)
│   └── raw/              # Archivos parquet generados localmente (ignorado en Git)
├── .env                  # Variables de entorno locales y llaves criptográficas (secreto)
├── .gitignore            # Archivos excluidos del control de versiones
└── requirements.txt      # Dependencias del proyecto


⚙️ Tecnologías Utilizadas

    Lenguaje: Python 3.12

    Librerías Clave: fastf1, pandas, google-cloud-storage, python-dotenv

    Cloud Infrastructure: Google Cloud Storage (GCS)

    CI/CD & Orquestación: GitHub Actions

🚀 Modos de Ejecución

El pipeline cuenta con una lógica inteligente de entorno que detecta la rama de Git sobre la cual se está trabajando:
🛠️ Modo Desarrollo (DEV_MODE = true)

Se activa automáticamente al ejecutar el pipeline desde cualquier rama distinta a main (como GCP-integration).

    Limita la extracción a 10 filas de muestra de los Rounds 1, 2 y 3.

    Sube los resultados al bucket bajo el prefijo dev_raw/ para evitar costos innecesarios y mantener limpio el entorno productivo.

🏁 Modo Producción (DEV_MODE = false)

Se ejecuta al realizar despliegues en la rama main.

    Procesa la temporada completa de 2026 de forma masiva.

    Almacena los archivos en la ruta de producción raw/ dentro del bucket de Google Cloud.

🔒 Seguridad y Buenas Prácticas

    Push Protection: Las credenciales de la cuenta de servicio de GCP (JSON) se gestionan estrictamente a través de un archivo .env local y mediante Repository Secrets en GitHub (GCP_SA_KEY), evitando la fuga o exposición de claves privadas en el historial público de Git.

    Control de Datos: Las carpetas de almacenamiento masivo y archivos temporales locales (data/) están estrictamente bloqueadas en el .gitignore para optimizar el peso del repositorio.