import logging
from extract import download_data, DATA_URL, RAW_DATA_PATH
from transform import transform_data, PROCESSED_DATA_PATH
from load import load_data, FINAL_DATA_PATH

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("Iniciando Pipeline ETL SNIC...")
    
    # Step 1: Extract
    if not download_data(DATA_URL, RAW_DATA_PATH):
        logging.error("Fallo en el paso de Extracción.")
        return
        
    # Step 2: Transform
    if not transform_data(RAW_DATA_PATH, PROCESSED_DATA_PATH):
        logging.error("Fallo en el paso de Transformación.")
        return
        
    # Step 3: Load (Local + Cloud)
    if not load_data(PROCESSED_DATA_PATH, FINAL_DATA_PATH):
        logging.error("Fallo en el paso de Carga.")
        return
        
    logging.info("Pipeline ETL SNIC completado exitosamente.")

if __name__ == "__main__":
    run_pipeline()
