import os


class FileDetector:
    # Magic numbers for common file types
    SIGNATURES = {
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'PK\x03\x04': 'ZIP/DOCX/XLSX',  # Office/ZIP files
        b'%PDF': 'PDF',
        b'\xef\xbb\xbf': 'UTF-8 BOM',
        b'Obj\x01': 'AVRO',
    }

    @staticmethod
    def detect_type(file_path: str) -> str:
        """Detects file type using magic numbers with extension fallback."""
        # Check if file exists first
        if not os.path.exists(file_path):
            return "UNKNOWN"
        
        # 1. Try Signature Detection if file exists
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                for sig, file_type in FileDetector.SIGNATURES.items():
                    if header.startswith(sig):
                        # Special handling for ZIP-based formats
                        if (file_type == 'ZIP/DOCX/XLSX' and
                                file_path.endswith('.xlsx')):
                            return 'XLSX'
                        return file_type
        except Exception:
            pass

        # 2. Fallback to Extension
        ext = os.path.splitext(file_path)[1].lower()
        extension_map = {
            '.csv': 'CSV',
            '.json': 'JSON',
            '.xml': 'XML',
            '.parquet': 'PARQUET',
            '.avro': 'AVRO',
            '.txt': 'TEXT'
        }

        return extension_map.get(ext, "UNKNOWN")
