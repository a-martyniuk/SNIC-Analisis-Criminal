# SNIC Análisis Criminal

Proyecto de análisis de datos criminales del SNIC (Sistema Nacional de Información Criminal) de Argentina.

## Descripción
Pipeline ETL (Extract, Transform, Load) para procesar estadísticas criminales anuales y generar analíticas en formato Parquet, con capacidades de integración en Google Cloud Platform (GCP).

## Estructura del Proyecto
- `src/`: Código fuente del pipeline ETL.
  - `extract.py`: Descarga de datos (con fallback a mock).
  - `transform.py`: Limpieza y transformación.
  - `load.py`: Carga a Parquet local, GCS y BigQuery.
  - `pipeline.py`: Orquestador principal.
- `tests/`: Pruebas unitarias.
- `notebooks/`: Análisis exploratorio (EDA).
- `data/`: Datos crudos y procesados (ignorado en git).

## Instalación
1. Clonar el repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución
Para correr el pipeline completo:
```bash
python src/pipeline.py
```

## Pruebas
Ejecutar la suite de pruebas automatizadas:
```bash
pytest tests/
```

## Configuración Cloud (Opcional)
Para habilitar la carga a GCP, configurar las variables de entorno:
- `GCS_BUCKET_NAME`: Nombre del bucket de almacenamiento.
- `BQ_DATASET_ID`: ID del dataset de BigQuery.
- `BQ_TABLE_ID`: ID de la tabla (default: `snic_analytics`).
