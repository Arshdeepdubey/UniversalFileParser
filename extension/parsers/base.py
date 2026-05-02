from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> pd.DataFrame:
        """Parses the file and returns a Pandas DataFrame."""
        pass