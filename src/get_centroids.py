import requests
import json
import pandas as pd
import os

url = "https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.2/download/provincias.json"
output_csv = "data/provincias_centroids.csv"

def get_centroids():
    try:
        print(f"Descargando desde {url}...")
        # Disable SSL verify for gob.ar just in case
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get(url, verify=False, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        
        # The structure is {"provincias": [{"nombre": "...", "centroide": {"lat": ..., "lon": ...}}, ...]}
        
        provinces_list = []
        for p in data['provincias']:
            # Normalize names to match SNIC data if possible
            name = p['nombre']
            lat = p['centroide']['lat']
            lon = p['centroide']['lon']
            
            # Manual fixes for common discrepancies known in SNIC data
            # SNIC usually has "Ciudad Autónoma de Buenos Aires", "Buenos Aires", etc.
            # Long name for TdF in SNIC might be just "Tierra del Fuego" or full.
            # We will check mapping later, but let's try to be standard.
            if name == "Tierra del Fuego, Antártida e Islas del Atlántico Sur": 
                # Let's add ONLY the short version for now as TdF sometimes is tricky
                provinces_list.append({'provincia_nombre': "Tierra del Fuego", 'lat': lat, 'lon': lon})
                # And usually allow the full name too just in case
            
            provinces_list.append({'provincia_nombre': name, 'lat': lat, 'lon': lon})
            
        df = pd.DataFrame(provinces_list)
        df.to_csv(output_csv, index=False)
        print(f"✅ Centroides guardados en {output_csv}")
        print(df.head())
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    get_centroids()
