# 📊 Panel de Análisis Criminal SNIC

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://alexismartyniuk-snic.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Live Demo:** [https://alexismartyniuk-snic.streamlit.app/](https://alexismartyniuk-snic.streamlit.app/)

Una plataforma de inteligencia de datos moderna para la exploración y visualización de estadísticas de seguridad ciudadana en Argentina, basada en datos oficiales del **SNIC (Sistema Nacional de Información Criminal)**.

## 🚀 Características Principales

*   **🌎 Tablero Interactivo (Dashboard):** Visualización de KPIs, rankings provinciales y evolución temporal.
*   **🔎 Mapa Coroplético:** Análisis geoespacial con geometrías oficiales y métricas duales (Tasa c/100k hab vs Cantidad Total).
*   **⚔️ Comparador de Entidades:** Herramienta "Versus" para comparar métricas y tendencias entre dos provincias lado a lado.
*   **🔮 Predicciones (ML):** Modelo de regresión integrado para proyectar tendencias criminales futuras.
*   **🧠 Insights Automáticos:** Detección inteligente de patrones (delitos más frecuentes, variaciones interanuales récord).

## 🛠️ Stack Tecnológico

Este proyecto utiliza un stack moderno, gratuito y de código abierto:

*   **Core:** Python 3.11+
*   **Datos:** Pandas, Parquet (Almacenamiento eficiente).
*   **Visualización:** Streamlit, Plotly Express.
*   **Infraestructura:** Docker, GitHub Actions (CI/CD).

## 📂 Estructura del Proyecto

```
.
├── src/                # Código fuente principal
│   ├── app.py          # Aplicación Streamlit (Dashboard)
│   ├── pipeline.py     # Orquestador ETL
│   ├── model.py        # Motor de Machine Learning
│   └── ...
├── data/               # Gestión de datos (Raw/Processed/Final)
├── docs/               # Documentación y Guías (DEPLOY.md, walkthrough.md)
├── tests/              # Tests automatizados
├── Dockerfile          # Definición de contenedor para despliegue
└── requirements.txt    # Dependencias del proyecto
```

## ⚡ Instalación y Ejecución Local

Tienes dos formas de correr este proyecto en tu máquina:

### Opción A: Docker (Recomendada)
Si tienes Docker instalado, simplemente corre:

```bash
docker-compose up --build
```
La aplicación estará disponible en `http://localhost:8501`.

### Opción B: Python Tradicional

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/snic-analisis-criminal.git
    cd snic-analisis-criminal
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generar los datos (ETL):**
    ```bash
    python src/pipeline.py
    ```

4.  **Iniciar el Dashboard:**
    ```bash
    streamlit run src/app.py
    ```

## 📖 Despliegue (Deploy)

Consulta el archivo [DEPLOY.md](DEPLOY.md) para ver guías detalladas sobre cómo desplegar este proyecto gratis en **Streamlit Community Cloud** o en tu propio servidor.

## 📄 Créditos y Datos

*   **Fuente de Datos:** [Dirección Nacional de Estadística Criminal - Bases de Datos](https://www.argentina.gob.ar/seguridad/estadisticascriminales/bases-de-datos).
*   **Procesamiento Geográfico:** APIs de GeoRef e INDEC (Censo 2022).
*   **Desarrollado por:** Alexis Martyniuk.
