import pandas as pd
from .base import BaseParser
import logging

logger = logging.getLogger("AvroParser")

# Try to import avro, but make it optional
try:
    import avro.datafile
    import avro.io
    AVRO_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    AVRO_AVAILABLE = False
    logger.warning("avro-python3 not available. AvroParser will not be functional.")

class CSVParser(BaseParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

class JSONParser(BaseParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        return pd.read_json(file_path)

class ParquetParser(BaseParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        return pd.read_parquet(file_path)

class XLSXParser(BaseParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        return pd.read_excel(file_path, engine='openpyxl')

class AvroParser(BaseParser):
    def parse(self, file_path: str) -> pd.DataFrame:
        try:
            # We use pandavro because it handles the Avro schema automatically
            import pandavro as pdv
            return pdv.read_avro(file_path)
        except ImportError:
            logger.error("Pandavro/Fastavro not found.")
            raise ImportError("Please run: pip install pandavro fastavro")
        except Exception as e:
            logger.error(f"Avro parsing failed: {e}")
            raise e