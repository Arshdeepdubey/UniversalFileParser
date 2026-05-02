import pandas as pd
from .base import BaseParser
import logging

logger = logging.getLogger("ParserFactory")

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
        if not AVRO_AVAILABLE:
            raise RuntimeError("avro-python3 is not available. Please install it with: pip install avro-python3")
        
        try:
            # Read Avro file using avro-python3
            records = []
            with avro.datafile.DataFileReader(open(file_path, 'rb'), avro.io.DatumReader()) as reader:
                for record in reader:
                    records.append(record)
            
            if not records:
                logger.warning(f"Avro file {file_path} is empty.")
                return pd.DataFrame()
            
            df = pd.DataFrame(records)
            return df
        except Exception as e:
            logger.error(f"Failed to parse Avro: {str(e)}")
            raise ValueError(f"Invalid Avro format or schema mismatch: {str(e)}")