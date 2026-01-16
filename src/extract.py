import requests
import os
import logging
import pandas as pd
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
DATA_URL = os.getenv("SNIC_DATA_URL", "https://cloud-snic.minseg.gob.ar/Bases/SNIC/snic-departamentos-anual.csv") 
RAW_DATA_PATH = "data/raw/snic_data.csv"

def generate_mock_data(output_path: str):
    """Generates mock SNIC data and saves it to output_path."""
    logging.info("Generando datos simulados...")
    
    # Create a mock dataset based on standard SNIC structure
    data = {
        'anio': [2020, 2020, 2021, 2021] * 5,
        'provincia_nombre': ['Buenos Aires', 'Córdoba', 'Santa Fe', 'Mendoza'] * 5,
        'codigo_delito_snic_nombre': ['Homicidios dolosos', 'Robos', 'Hurtos', 'Amenazas'] * 5,
        'cantidad_hechos': [random.randint(10, 1000) for _ in range(20)],
        'cantidad_victimas': [random.randint(10, 1000) for _ in range(20)]
    }
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info(f"Datos simulados guardados en {output_path}")

def download_data(url: str, output_path: str):
    """Downloads data from URL and saves to output_path. Falls back to mock data on failure."""
    logging.info(f"Intentando descargar desde {url}...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
            
        logging.info(f"Descarga completada. Guardado en {output_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        logging.warning(f"Error descargando datos: {e}")
        logging.warning("Revertiendo a generación de datos simulados.")
        generate_mock_data(output_path)
        return True

if __name__ == "__main__":
    download_data(DATA_URL, RAW_DATA_PATH)
