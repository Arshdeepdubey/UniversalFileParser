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
    assert "name" in result["columns"]

@pytest.mark.skipif(
    not os.path.exists("tests/assets/test.avro"),
    reason="test.avro not available (avro-python3 not installed)"
)
def test_avro_parsing(manager):
    result = manager.parse_file("tests/assets/test.avro")
    assert result["status"] == "success"
    assert result["detected_type"] == "AVRO"
    assert result["rows"] == 2
    # Check if nested fields were handled
    assert "details" in result["columns"]