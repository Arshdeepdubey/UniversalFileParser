import pytest
import os
from extension.main import ExtensionManager

@pytest.fixture
def manager():
    m = ExtensionManager()
    m.activate()
    return m

def test_json_parsing(manager):
    result = manager.parse_file("tests/assets/test.json")
    assert result["status"] == "success"
    assert result["detected_type"] == "JSON"
    assert len(result["preview"]) > 0
    # Use the cleaned/normalized column name
    assert "name" in result["columns"]

def test_avro_parsing(manager):
    result = manager.parse_file("tests/assets/test.avro")
    assert result["status"] == "success"
    assert result["detected_type"] == "AVRO"
    assert result["rows"] == 2
    
    # FIX: Phase 4 flattening transformed 'details' into these columns
    assert "details_dept" in result["columns"]
    assert "details_site" in result["columns"]
    # Ensure the original nested 'details' was dropped
    assert "details" not in result["columns"]