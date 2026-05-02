import pytest
import os
from extension.detector import FileDetector

def test_extension_fallback(tmp_path):
    d = tmp_path / "test.csv"
    d.write_text("col1,col2\nval1,val2")
    assert FileDetector.detect_type(str(d)) == "CSV"

def test_pdf_signature(tmp_path):
    d = tmp_path / "fake.pdf"
    # Write the PDF magic number
    d.write_bytes(b"%PDF-1.4\n%...")
    assert FileDetector.detect_type(str(d)) == "PDF"

def test_unknown_type(tmp_path):
    d = tmp_path / "random.xyz"
    d.write_text("random content")
    assert FileDetector.detect_type(str(d)) == "UNKNOWN"