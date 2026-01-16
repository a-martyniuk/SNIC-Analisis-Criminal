import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.load import load_data, upload_to_gcs, upload_to_bigquery
import os

TEST_INPUT = "tests/data/processed/snic_clean.csv"
TEST_OUTPUT = "tests/data/final/snic_analytics.parquet"

@pytest.fixture
def mock_clients():
    with patch('src.load.storage.Client') as mock_storage, \
         patch('src.load.bigquery.Client') as mock_bq:
        yield mock_storage, mock_bq

@pytest.fixture
def clean_test_files():
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    # create dummy input
    os.makedirs(os.path.dirname(TEST_INPUT), exist_ok=True)
    pd.DataFrame({'col': [1]}).to_csv(TEST_INPUT, index=False)
    yield
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)

def test_upload_to_gcs_success(mock_clients):
    mock_storage, _ = mock_clients
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_storage.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    result = upload_to_gcs("dummy_path", "test-bucket", "dest_blob")
    
    assert result is True
    mock_storage.return_value.bucket.assert_called_with("test-bucket")
    mock_bucket.blob.assert_called_with("dest_blob")
    mock_blob.upload_from_filename.assert_called_with("dummy_path")

def test_upload_to_bigquery_success(mock_clients):
    _, mock_bq = mock_clients
    mock_client_instance = mock_bq.return_value
    mock_client_instance.project = "test-project"
    
    df = pd.DataFrame({'a': [1]})
    result = upload_to_bigquery(df, "test_dataset", "test_table")
    
    assert result is True
    mock_client_instance.load_table_from_dataframe.assert_called_once()
    # Check table ref construction
    args, _ = mock_client_instance.load_table_from_dataframe.call_args
    assert args[1] == "test-project.test_dataset.test_table"

@patch('os.getenv')
def test_load_data_with_cloud(mock_getenv, mock_clients, clean_test_files):
    # Configure env vars to trigger cloud upload
    def getenv_side_effect(key, default=None):
        if key == "GCS_BUCKET_NAME": return "my-bucket"
        if key == "BQ_DATASET_ID": return "my_dataset"
        return default
    mock_getenv.side_effect = getenv_side_effect
    
    result = load_data(TEST_INPUT, TEST_OUTPUT)
    
    assert result is True
    
    # Verify GCS upload called (via mock verification logic or we can spy on upload_to_gcs)
    # Since we are mocking the Clients inside src.load, we can check if they were instantiated
    mock_storage, mock_bq = mock_clients
    mock_storage.return_value.bucket.assert_called()
    mock_bq.return_value.load_table_from_dataframe.assert_called()
