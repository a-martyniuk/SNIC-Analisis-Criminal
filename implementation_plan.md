# Plan de Análisis Exploratorio de Datos (EDA) - SNIC

Este plan detalla la expansión del notebook de análisis `notebooks/01_eda.ipynb` para aprovechar los datos reales del SNIC (2000-2024).

## Objetivo
Realizar un análisis descriptivo profundo de las estadísticas criminales de Argentina, respondiendo preguntas clave sobre tendencias temporales, distribución geográfica y tipologías delictivas.

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
- (Opcional) Ejecución manual si el usuario provee credenciales (no bloqueante).


