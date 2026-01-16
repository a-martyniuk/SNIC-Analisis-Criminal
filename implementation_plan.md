# Plan de Análisis Exploratorio de Datos (EDA) - SNIC

Este plan detalla la expansión del notebook de análisis `notebooks/01_eda.ipynb` para aprovechar los datos reales del SNIC (2000-2024).

## Objetivo
Realizar un análisis descriptivo profundo de las estadísticas criminales de Argentina, respondiendo preguntas clave sobre tendencias temporales, distribución geográfica y tipologías delictivas. Además, disponibilizar estos resultados a través de un dashboard interactivo.

## Revisiones del Usuario
> [!NOTE]
> Todo el contenido del notebook y los gráficos se generarán en español para mantener consistencia con la documentación del proyecto.

## Cambios Propuestos


## Estado Actual: EDA Completado
Se ha verificado la ejecución correcta del análisis exploratorio (`notebooks/01_eda.py`) y la generación de gráficos.

## Fase 2: Robustez del Pipeline (Hardening)

### Objetivo
Asegurar la estabilidad y mantenibilidad del pipeline ETL mediante pruebas unitarias y limpieza de código.

### Cambios Propuestos

#### Estructura de Pruebas
Se creará un directorio `tests/` para alojar las pruebas unitarias.

#### [NEW] [test_extract.py](file:///d:/Projects/SNIC-Analisis-Criminal/tests/test_extract.py)
- **Objetivo**: Probar la lógica de descarga y manejo de fallos.
- **Estrategia**: Mocker `requests.get` para simular respuestas exitosas y fallidas (fallback a datos mock).

#### [NEW] [test_transform.py](file:///d:/Projects/SNIC-Analisis-Criminal/tests/test_transform.py)
- **Objetivo**: Verificar la limpieza y transformación de datos.
- **Estrategia**: Crear un DataFrame de prueba en memoria y verificar que `transform_data` maneje correctamente nulos, tipos de datos y columnas requeridas.

#### Limpieza de Código
Eliminar scripts temporales de depuración que ya no son necesarios:
- `src/debug_bytes.py`
- `src/inspect_bytes.py`
- `debug_values.txt`
- `src/find_non_ascii.py` (si ya no se usa)
- `src/diagnose_encoding.py` (si ya no se usa)

## Plan de Verificación

### Pruebas Automatizadas
Ejecutar el suite de pruebas con `pytest`:
```bash
pytest tests/
```

## Fase 3: Integración Cloud (Google Cloud Platform)

### Objetivo
Extender el pipeline para persistir los datos procesados en la nube (GCS y BigQuery), cumpliendo con el objetivo de un "pipeline end-to-end en la nube".

### Cambios Propuestos

#### [MODIFY] [load.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/load.py)
- **Funcionalidad GCS**: Agregar capacidad para subir el archivo parquet a un bucket de Google Cloud Storage.
- **Funcionalidad BigQuery**: Agregar capacidad para cargar el DataFrame directamente a una tabla de BigQuery.
- **Configuración**: Utilizar variables de entorno (`GCP_PROJECT`, `GCS_BUCKET_NAME`, `BQ_DATASET_ID`) para la configuración.

#### [NEW] [tests/test_cloud.py](file:///d:/Projects/SNIC-Analisis-Criminal/tests/test_cloud.py)
- **Objetivo**: Mockear las librerías `google.cloud` para verificar que las funciones de carga se llamen con los parámetros correctos.

## Plan de Verificación
- Ejecutar pruebas unitarias mockeadas.
## Fase 4: Visualización (Dashboard)

### Objetivo
Crear una aplicación web interactiva utilizando Streamlit para explorar los datos de manera dinámica, permitiendo filtrar por año, provincia y tipo de delito.

### Cambios Propuestos

#### [MODIFY] [requirements.txt](file:///d:/Projects/SNIC-Analisis-Criminal/requirements.txt)
- Agregar `streamlit`
- Agregar `plotly` (para gráficos interactivos avanzados)

#### [NEW] [src/app.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/app.py)
- **Funcionalidad**:
    - Carga de datos desde `data/final/snic_analytics.parquet` (o fallback a procesados/raw).
    - Sidebar con filtros (Año, Provincia, Delito).
    - KPIs principales: Total Hechos, Total Víctimas, Promedio por Provincia.
    - Gráficos:
        - Evolución temporal de delitos.
        - Mapa de calor o geográfico (si hay datos geo).
        - Ranking de provincias por tasa delictiva.

## Plan de Verificación

### Pruebas Automatizadas
- Ejecutar el suite de pruebas existente: `pytest tests/`

### Verificación Manual (Dashboard)
- Ejecutar la aplicación:
  ```bash
  streamlit run src/app.py
  ```
- Verificar KPIs: Comparar números con el EDA estático.

## Fase 5: Contenerización (Docker)

### Objetivo
Empaquetar la aplicación y el pipeline en contenedores Docker para asegurar la portabilidad y facilitar el despliegue en cualquier entorno.

### Cambios Propuestos

#### [NEW] [Dockerfile](file:///d:/Projects/SNIC-Analisis-Criminal/Dockerfile)
- Base image: `python:3.10-slim`
- Instalación de dependencias desde `requirements.txt`.
- Copia del código fuente (`src/`).
- Comando de inicio por defecto: Lanzar el dashboard Streamlit.

#### [NEW] [.dockerignore](file:///d:/Projects/SNIC-Analisis-Criminal/.dockerignore)
- Excluir `data/` (los datos no deben estar en la imagen base por tamaño/seguridad, se montarán como volumen).
- Excluir `.git`, `__pycache__`, `venv`.

#### [NEW] [docker-compose.yml](file:///d:/Projects/SNIC-Analisis-Criminal/docker-compose.yml)
- Servicio `app`:
    - Build: `.`
    - Ports: `8501:8501`
    - Volumes: `./data:/app/data` (Persistencia de datos).

## Plan de Verificación
- Construir la imagen: `docker-compose build`
- Levantar el servicio: `docker-compose up`
- Verificar acceso en `http://localhost:8501`.

## Fase 6: Automatización CI/CD

### Objetivo
Asegurar que cada cambio en el código no solo pase las pruebas unitarias, sino que también sea empaquetable en un contenedor Docker válido.

### Cambios Propuestos

#### [MODIFY] [.github/workflows/ci.yml](file:///d:/Projects/SNIC-Analisis-Criminal/.github/workflows/ci.yml)
- **Job de Build Docker**: Agregar un paso para construir la imagen Docker.
- Esto garantiza que el `Dockerfile` siempre sea válido y que todas las dependencias se instalen correctamente en el entorno Linux del contenedor.

### Snippet Propuesto
```yaml
    - name: Build Docker image
      run: docker build . --file Dockerfile --tag snic-app:latest
```

## Plan de Verificación
- Commit y Push de los cambios.
- Verificar que la Action se ejecute exitosamente en GitHub (simulado localmente).

## Fase 7: Modelo Predictivo (Forecasting)

### Objetivo
Implementar un modelo simple de Machine Learning para predecir la tendencia criminal del próximo año basándose en datos históricos.

### Cambios Propuestos

#### [MODIFY] [requirements.txt](file:///d:/Projects/SNIC-Analisis-Criminal/requirements.txt)
- Agregar `scikit-learn`.

#### [NEW] [src/model.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/model.py)
- **Función `train_and_predict(df)`**:
    - Prepara datos de series temporales (Año -> Cantidad).
    - Entrena un modelo de Regresión Lineal (o Random Forest si hay suficientes datos).
    - Genera predicciones para el año futuro (ej. 2025).

#### [MODIFY] [src/app.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/app.py)
- Agregar nueva Pestaña "🔮 Predicciones".
- Visualizar la curva histórica + la proyección futura con intervalo de incertidumbre.

## Plan de Verificación
- Verificar que el modelo no arroje errores con datos limitados.
- Visualizar la predicción en el Dashboard.

## Fase 8: Mejoras UX/UI

### Objetivo
Mejorar la legibilidad de las etiquetas (especialmente tipos de delitos largos) y pulir la estética general del dashboard.

### Cambios Propuestos

#### [MODIFY] [src/app.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/app.py)
- **Mapeo de Nombres Cortos**:
    - Crear un diccionario o función para truncar/renombrar categorías largas (ej. "Homicidios Dolosos" -> "Homicidios D.").
    - Aplicar este mapeo al cargar los datos para que afecte tanto a los filtros como a los gráficos.
- **Estética de Gráficos**:
    - Configurar `layout` de Plotly para manejar márgenes automáticos (`automargin`).
    - Usar una paleta de colores consistente.
    - Asegurar que los gráficos de barras usen orientación horizontal cuando hay muchas categorías.

## Plan de Verificación
- Verificar visualmente que los filtros en el sidebar no corten texto importante.
- Verificar que los ejes de los gráficos sean legibles.

## Fase 9: Mapa Geográfico

### Objetivo
Reemplazar o complementar el heatmap matricial con un mapa geográfico real de Argentina (Choropleth) que pinte las provincias según la intensidad del delito.

### Recursos
- **GeoJSON**: Descargar `provincias.geojson` desde fuente abierta (ej. GitHub artifact).
- **Normalización**: Asegurar que los nombres del GeoJSON coincidan con los del dataset del SNIC (ej. "Tierra del Fuego..." vs "Tierra del Fuego").

### Cambios Propuestos

#### [NEW] [data/provincias.geojson](file:///d:/Projects/SNIC-Analisis-Criminal/data/provincias.geojson)
- Archivo estático con las geometrías.

#### [MODIFY] [src/app.py](file:///d:/Projects/SNIC-Analisis-Criminal/src/app.py)
- Cargar GeoJSON.
- **Tab 3**: Cambiar `px.density_heatmap` por `px.choropleth`.
- Mapear nombres de provincias si hay discrepancias.



