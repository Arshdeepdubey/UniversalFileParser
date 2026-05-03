import os


class FileDetector:
    # Magic numbers for common file types
    SIGNATURES = {
        b'Obj\x01': 'AVRO',
        b'PAR1': 'PARQUET',
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'PK\x03\x04': 'XLSX',
        b'%PDF': 'PDF',
    }

    @staticmethod
    def detect_type(file_path: str) -> str:
        """Detects file type using magic numbers with extension fallback."""
        # 1. Guard: If the file doesn't exist, we cannot safely detect its type
        if not os.path.exists(file_path):
            return "UNKNOWN"

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

        # 2. Try Signature Detection
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                for sig, ftype in FileDetector.SIGNATURES.items():
                    if header.startswith(sig):
                        # Special check for XLSX (OpenXML) files
                        if ftype == 'XLSX' and not ext == '.xlsx':
                            continue
                        return ftype
        except Exception:
            pass

        # 3. Fallback to Extension
        return extension_map.get(ext, "UNKNOWN")