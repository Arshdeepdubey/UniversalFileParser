import pytest
import os
from extension.detector import FileDetector

@pytest.fixture
def create_mock_file(tmp_path):
    """Helper to create files with specific content/headers."""
    def _create(filename, content, is_binary=False):
        file_path = tmp_path / filename
        if is_binary:
            file_path.write_bytes(content)
        else:
            file_path.write_text(content)
        return str(file_path)
    return _create

## 1. Magic Number (Signature) Tests
def test_detect_pdf_signature(create_mock_file):
    # PDF magic number: %PDF
    path = create_mock_file("report.txt", b"%PDF-1.4\n", is_binary=True)
    assert FileDetector.detect_type(path) == "PDF"

def test_detect_avro_signature(create_mock_file):
    # Avro magic number: Obj\x01
    path = create_mock_file("data.bin", b"Obj\x01header", is_binary=True)
    assert FileDetector.detect_type(path) == "AVRO"

## 2. Extension Fallback Tests
def test_detect_csv_extension(create_mock_file):
    path = create_mock_file("data.csv", "id,name\n1,Gemini")
    assert FileDetector.detect_type(path) == "CSV"

def test_detect_parquet_extension(create_mock_file):
    path = create_mock_file("records.parquet", "binary_content")
    assert FileDetector.detect_type(path) == "PARQUET"

## 3. Edge Cases
def test_detect_unknown_format(create_mock_file):
    path = create_mock_file("mystery.xyz", "random data")
    assert FileDetector.detect_type(path) == "UNKNOWN"

def test_detect_non_existent_file():
    assert FileDetector.detect_type("non_existent.json") == "UNKNOWN"

def test_detect_xlsx_logic(create_mock_file):
    # XLSX is technically a ZIP file. We check if it handles the overlap.
    path = create_mock_file("spreadsheet.xlsx", b"PK\x03\x04", is_binary=True)
    assert FileDetector.detect_type(path) == "XLSX"