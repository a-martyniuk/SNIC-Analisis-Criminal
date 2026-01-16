import pandas as pd
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RAW_DATA_PATH = "data/raw/snic_data.csv"
PROCESSED_DATA_PATH = "data/processed/snic_clean.csv"

def transform_data(input_path: str, output_path: str):
    """Cleans and transforms raw SNIC data."""
    logging.info(f"Cargando datos crudos desde {input_path}...")
    
    if not os.path.exists(input_path):
        logging.error(f"Archivo de entrada no encontrado: {input_path}")
        return False
        
    try:
        df = pd.read_csv(input_path, sep=';', encoding='utf-8')
    except UnicodeDecodeError as e:
        logging.error(f"Fallo al leer archivo con codificación UTF-8: {e}")
        return False
    
    # 1. Basic Cleaning
    # Drop rows with critical missing values if necessary, though mock data should be clean
    df.dropna(subset=['anio', 'provincia_nombre'], inplace=True)
    
    # 2. Type Conversion
    df['anio'] = df['anio'].astype(int)
    
    # 3. Standardization
    # Example: specific text cleaning or category mapping could go here
    # df['provincia_nombre'] = df['provincia_nombre'].str.strip().str.title()
    
    # 4. Aggregation (Optional - purely for demonstrative structure)
    # Keeping raw granularity for now, but ensure columns are consistent
    required_columns = ['anio', 'provincia_nombre', 'codigo_delito_snic_nombre', 'cantidad_hechos', 'cantidad_victimas']
    if not all(col in df.columns for col in required_columns):
         logging.warning(f"Faltan columnas en datos de entrada. Disponibles: {df.columns}")
    
    logging.info(f"Datos transformados. Dimensiones: {df.shape}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    logging.info(f"Datos procesados guardados en {output_path}")
    return True

if __name__ == "__main__":
    transform_data(RAW_DATA_PATH, PROCESSED_DATA_PATH)
