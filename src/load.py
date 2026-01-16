import pandas as pd
import logging
import os
from google.cloud import storage, bigquery
from google.api_core.exceptions import GoogleAPIError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROCESSED_DATA_PATH = "data/processed/snic_clean.csv"
FINAL_DATA_PATH = "data/final/snic_analytics.parquet"

def upload_to_gcs(file_path: str, bucket_name: str, destination_blob_name: str):
    """Uploads a file to Google Cloud Storage."""
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        logging.info(f"Archivo {file_path} subido a gs://{bucket_name}/{destination_blob_name}")
        return True
    except GoogleAPIError as e:
        logging.error(f"Fallo al subir a GCS: {e}")
        return False

def upload_to_bigquery(df: pd.DataFrame, dataset_id: str, table_id: str):
    """Uploads a DataFrame to a BigQuery table."""
    try:
        client = bigquery.Client()
        table_ref = f"{client.project}.{dataset_id}.{table_id}"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE", # Complete overwrite for analytics tables
        )
        
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result() # Wait for job to complete
        
        logging.info(f"Cargadas {len(df)} filas en {table_ref}")
        return True
    except GoogleAPIError as e:
        logging.error(f"Fallo al subir a BigQuery: {e}")
        return False

def load_data(input_path: str, output_path: str):
    """Loads processed data into local Parquet and optionally to Cloud."""
    logging.info(f"Cargando datos procesados desde {input_path}...")
    
    if not os.path.exists(input_path):
        logging.error(f"Archivo de entrada no encontrado: {input_path}")
        return False
        
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception as e:
        logging.error(f"Fallo al leer CSV: {e}")
        return False
    
    # 1. Save to Local Parquet
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_parquet(output_path, index=False)
        logging.info(f"Datos cargados exitosamente en {output_path}")
    except Exception as e:
        logging.error(f"Fallo al guardar parquet local: {e}")
        return False

    # 2. Upload to GCS (if configured)
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if bucket_name:
        blob_name = os.path.basename(output_path)
        upload_to_gcs(output_path, bucket_name, blob_name)
    
    # 3. Upload to BigQuery (if configured)
    bq_dataset = os.getenv("BQ_DATASET_ID")
    bq_table = os.getenv("BQ_TABLE_ID", "snic_analytics")
    if bq_dataset:
        upload_to_bigquery(df, bq_dataset, bq_table)
        
    return True

if __name__ == "__main__":
    load_data(PROCESSED_DATA_PATH, FINAL_DATA_PATH)
