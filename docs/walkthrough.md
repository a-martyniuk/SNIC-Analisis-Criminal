# Documentación del Proyecto: Panel de Análisis Criminal SNIC

Este documento detalla la arquitectura, implementación y características del sistema de Análisis Criminal SNIC. El proyecto integra un pipeline ETL robusto, análisis de datos avanzado y un dashboard interactivo de alto rendimiento para la visualización de estadísticas de seguridad en Argentina.

## 1. Arquitectura del Proyecto

El sistema está diseñado modularmente para asegurar escalabilidad y mantenibilidad:

-   **`src/`**: Núcleo del procesamiento (ETL y Dashboard).
    -   `extract.py`, `transform.py`, `load.py`: Componentes del pipeline de datos.
    -   `model.py`: Motor de Machine Learning para predicciones.
    -   `app.py`: Aplicación Web interactiva (Streamlit).
-   **`data/`**: Gestión de datos en capas (raw, processed, final).
-   **`notebooks/`**: Análisis exploratorio y prototipeo.
-   **Docker**: Contenerización completa para despliegue agnóstico del entorno.

## 2. Pipeline ETL (Extraction, Transformation, Load)

Se implementó un flujo de datos optimizado para manejar la complejidad de las estadísticas criminales:

1.  **Extracción (`src/extract.py`)**:
    -   Conexión directa con fuentes oficiales del SNIC.
    -   Gestión automática de descargas de datos departamentales y provinciales.

2.  **Transformación (`src/transform.py`)**:
    -   Limpieza y normalización de datasets crudos.
    -   Estandarización de nombres de provincias y tipos de delitos.
    -   Manejo de codificaciones complejas (`latin-1`) y formatos CSV variados.

3.  **Carga (`src/load.py`)**:
    -   Generación de archivos `.parquet` optimizados para lectura rápida en el dashboard.

**Ejecución:**
```bash
python src/pipeline.py
```

## 3. Dashboard Interactivo (Streamlit)

La interfaz de usuario ha sido diseñada con un enfoque en **UX/UI moderno y profesional** ("Midnight Blue Theme"), priorizando la claridad de los datos y la toma de decisiones.

### Características Principales

*   **🌎 Resumen General**:
    *   **KPIs de Alto Impacto**: Tarjetas con métricas clave (Total Hechos, Tasa c/100k) y comparativas interanuales automáticas.
    *   **Insights Inteligentes**: Detección automática de patrones (delito más frecuente, provincia con mayor aumento/descenso).
    *   **Filtros Jerárquicos**: Navegación fluida por Categoría -> Tipo de Delito -> Provincia -> Departamento.

*   **🔎 Detalle Geográfico (Mapa Coroplético)**:
    *   **Visualización Profesional**: Mapa interactivo basado en geometrías oficiales (GeoJSON/GeoRef).
    *   **Métricas Duales**: Selector dinámico para alternar entre **Tasa cada 100k habitantes** (intensidad real) y **Cantidad Total** (volumen).
    *   **Estilo Dark Matter**: Integración estética perfecta con el tema oscuro de la aplicación.

*   **⚔️ Comparador de Entidades**:
    *   **Modo Versus**: Comparación directa "Side-by-Side" entre dos provincias o jurisdicciones.
    *   **Normalización Demográfica**: Ajuste automático por población (Censo 2022) para comparaciones justas.
    *   **Gráficos Evolutivos**: Análisis de tendencias históricas comparadas.

*   **🔮 Modelo Predictivo**:
    *   **Forecasting en Tiempo Real**: Proyección de tendencias criminales futuras mediante modelos de regresión.
    *   **Interactividad**: Ajuste de horizonte temporal de predicción.

*   **📈 Tendencias y Datos**:
    *   Gráficos de área y líneas para evolución histórica.
    *   Tabla de datos crudos con capacidad de exportación a CSV.

### Ejecución Local
```bash
streamlit run src/app.py
```

## 4. Despliegue y CI/CD

El proyecto está listo para entornos de producción modernos:

*   **Docker**: `Dockerfile` y `docker-compose.yml` configurados para un despliegue en un solo comando (`docker-compose up --build`).
*   **GitHub Actions**: Pipeline de CI configurado para ejecutar tests unitarios y verificar la construcción de la imagen Docker en cada commit, asegurando la integridad del código.

## 5. Próximos Pasos Sugeridos

*   Incorporación de datos a nivel municipal para mayor granularidad.
*   Implementación de modelos de ML más complejos (ej. Prophet, LSTM) para capturar estacionalidad mensual.
*   Panel de autenticación de usuarios para gestión de accesos.
