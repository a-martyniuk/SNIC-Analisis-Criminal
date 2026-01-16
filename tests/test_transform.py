import pytest
import pandas as pd
import os
from src.transform import transform_data

# Test data
TEST_INPUT = "tests/data/raw/snic_data.csv"
TEST_OUTPUT = "tests/data/processed/snic_clean.csv"

@pytest.fixture
def clean_test_files():
    # Clean up before and after
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)
    yield
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)

def create_sample_csv(path):
    data = {
        'anio': [2022, 2023, None],
        'provincia_nombre': ['Buenos Aires', 'Córdoba', None],
        'codigo_delito_snic_nombre': ['Robo', 'Hurto', 'Robo'],
        'cantidad_hechos': [10, 20, 5],
        'cantidad_victimas': [10, 20, 5]
    }
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, sep=';', index=False, encoding='utf-8')

def test_transform_data_success(clean_test_files):
    create_sample_csv(TEST_INPUT)
    
    result = transform_data(TEST_INPUT, TEST_OUTPUT)
    
    assert result is True
    assert os.path.exists(TEST_OUTPUT)
    
    # Verify content
    df = pd.read_csv(TEST_OUTPUT)
    
    # Check that nulls were dropped (one row with nulls)
    assert len(df) == 2
    
    # Check type conversion
    assert df['anio'].dtype == 'int64'

def test_transform_data_missing_input(clean_test_files):
    result = transform_data("non_existent_file.csv", TEST_OUTPUT)
    assert result is False
