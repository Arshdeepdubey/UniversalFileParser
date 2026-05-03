import pytest
import pandas as pd
from extension.main import ExtensionManager

@pytest.fixture
def manager():
    m = ExtensionManager()
    m.activate()
    return m

def test_full_pipeline_cleaning_and_flattening(manager, tmp_path):
    """Verifies that a 'dirty' file is parsed, snake_cased, and flattened."""
    # 1. Create a 'dirty' CSV with nested-looking headers and spaces
    dirty_csv = tmp_path / "dirty_data.csv"
    dirty_csv.write_text("User ID,First Name,Active Status\n101,Arshdeep,True")

    # 2. Run the pipeline
    result = manager.parse_file(str(dirty_csv))

    # 3. Assertions for Normalization (Phase 4)
    assert result["status"] == "success"
    # 'User ID' should become 'user_id'
    assert "user_id" in result["columns"]
    assert "first_name" in result["columns"]
    assert "active_status" in result["columns"]
    assert "User ID" not in result["columns"]

def test_avro_flattening_integration(manager):
    """Verifies that the Avro file generated in Phase 3 is now flattened."""
    # This assumes you ran the generate_test_data.py script earlier
    avro_path = "tests/assets/test.avro"
    
    result = manager.parse_file(avro_path)
    
    assert result["status"] == "success"
    # In Phase 3, we had a 'details' column. 
    # In Phase 4, it should be 'details_dept' and 'details_site'
    assert "details_dept" in result["columns"]
    assert "details_site" in result["columns"]
    assert "details" not in result["columns"]