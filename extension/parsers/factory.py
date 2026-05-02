from .implementations import (
    CSVParser, JSONParser, ParquetParser, XLSXParser, AvroParser
)

class ParserFactory:
    _parsers = {
        "CSV": CSVParser(),
        "JSON": JSONParser(),
        "PARQUET": ParquetParser(),
        "XLSX": XLSXParser(),
        "AVRO": AvroParser(),
    }

    @staticmethod
    def get_parser(file_type: str):
        return ParserFactory._parsers.get(file_type)