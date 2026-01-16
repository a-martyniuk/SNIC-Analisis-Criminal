import pandas as pd
import os

DATA_PATH = "data/final/snic_analytics.parquet"
FALLBACK_DATA_PATH = "data/processed/snic_clean.csv"

if os.path.exists(DATA_PATH):
    print(f"Reading {DATA_PATH}...")
    df = pd.read_parquet(DATA_PATH)
elif os.path.exists(FALLBACK_DATA_PATH):
    print(f"Reading {FALLBACK_DATA_PATH}...")
    df = pd.read_csv(FALLBACK_DATA_PATH)
else:
    print("No data found.")
    exit()

print("Columns:", df.columns.tolist())
print(df.head())
# Check typical names for departments
potentials = [c for c in df.columns if 'dep' in c.lower() or 'mun' in c.lower() or 'part' in c.lower()]
print("Potential department columns:", potentials)

# Check specifically for BA and CABA granularity
ba_data = df[df['provincia_nombre'].isin(['Buenos Aires', 'Ciudad Autónoma de Buenos Aires'])]
if not ba_data.empty:
    print("\nSample BA/CABA data:")
    print(ba_data.head())
