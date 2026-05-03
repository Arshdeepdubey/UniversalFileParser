import pytest
import pandas as pd
from extension.cleaner import DataCleaner

def test_column_normalization():
    df = pd.DataFrame({"First Name": [1], "Last-Name": [2], "AgeID": [3]})
    cleaned = DataCleaner.normalize_columns(df)
    assert list(cleaned.columns) == ["first_name", "last_name", "age_id"]

def test_flattening():
    # Simulate nested data (common in Avro/JSON)
    df = pd.DataFrame({
        "user": ["A", "B"],
        "info": [{"city": "Gurgaon", "zip": 122001}, {"city": "Delhi", "zip": 110001}]
    })
    cleaned = DataCleaner.flatten_nested_data(df)
    assert "info_city" in cleaned.columns
    assert "info_zip" in cleaned.columns
    assert "info" not in cleaned.columns

def test_missing_values():
    df = pd.DataFrame({"val": [1, None, float('nan')]})
    cleaned = DataCleaner.handle_missing_values(df)
    # Ensure they become 'None' for clean JSON serialization
    assert cleaned['val'].iloc[1] is None
    assert cleaned['val'].iloc[2] is None