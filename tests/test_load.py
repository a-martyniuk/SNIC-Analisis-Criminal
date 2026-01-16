import pytest
import pandas as pd
import os
from src.load import load_data

# Test data
TEST_INPUT = "tests/data/processed/snic_clean.csv"
TEST_OUTPUT = "tests/data/final/snic_analytics.parquet"

@pytest.fixture
def clean_test_files():
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)
    yield
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)

def create_processed_csv(path):
    data = {
        'anio': [2022],
        'provincia_nombre': ['Buenos Aires'],
        'cantidad_hechos': [100]
    }
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')

def test_load_data_success(clean_test_files):
    create_processed_csv(TEST_INPUT)
    
    result = load_data(TEST_INPUT, TEST_OUTPUT)
    
    assert result is True
    assert os.path.exists(TEST_OUTPUT)
    
    # Verify parquet can be read
    df = pd.read_parquet(TEST_OUTPUT)
    assert len(df) == 1
    assert df.iloc[0]['provincia_nombre'] == 'Buenos Aires'

def test_load_data_missing_input(clean_test_files):
    result = load_data("non_existent_file.csv", TEST_OUTPUT)
    assert result is False
