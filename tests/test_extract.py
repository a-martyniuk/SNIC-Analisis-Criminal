import pytest
from unittest.mock import patch, mock_open
import os
from src.extract import download_data, generate_mock_data

# Test data
TEST_URL = "http://example.com/data.csv"
TEST_OUTPUT = "tests/data/raw/test_data.csv"

@pytest.fixture
def clean_test_file():
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)
    yield
    if os.path.exists(TEST_OUTPUT):
        os.remove(TEST_OUTPUT)

@patch('requests.get')
def test_download_data_success(mock_get, clean_test_file):
    # Mock successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"anio,province\n2022,Buenos Aires"
    
    result = download_data(TEST_URL, TEST_OUTPUT)
    
    assert result is True
    assert os.path.exists(TEST_OUTPUT)
    with open(TEST_OUTPUT, 'r') as f:
        content = f.read()
    assert "2022,Buenos Aires" in content

@patch('src.extract.generate_mock_data')
@patch('requests.get')
def test_download_data_failure_fallback(mock_get, mock_generate_data, clean_test_file):
    # Mock failed response
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")
    
    result = download_data(TEST_URL, TEST_OUTPUT)
    
    assert result is True
    # Verify fallback was called
    mock_generate_data.assert_called_once_with(TEST_OUTPUT)
