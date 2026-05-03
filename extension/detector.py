import os


class FileDetector:
    # Core magic numbers
    SIGNATURES = {
        b'Obj\x01': 'AVRO',
        b'PAR1': 'PARQUET',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'PK\x03\x04': 'XLSX',  # ZIP-based (Excel, Docx)
        b'%PDF': 'PDF',
    }

    @staticmethod
    def detect_type(file_path: str) -> str:
        """Detects file type using magic numbers with extension fallback."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        extension_map = {
            '.csv': 'CSV',
            '.json': 'JSON',
            '.parquet': 'PARQUET',
            '.avro': 'AVRO',
            '.xlsx': 'XLSX',
            '.txt': 'TEXT'
        }

        # 1. Try Signature Detection if file exists
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(16)
                    for sig, ftype in FileDetector.SIGNATURES.items():
                        if header.startswith(sig):
                            # Special check: if it's a ZIP signature but .xlsx ext, it's XLSX
                            if ftype == 'XLSX' and not ext == '.xlsx':
                                continue
                            return ftype
            except Exception:
                pass

        # 2. Fallback to Extension
        return extension_map.get(ext, "UNKNOWN")