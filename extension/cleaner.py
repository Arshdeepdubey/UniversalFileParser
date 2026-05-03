import pandas as pd
import re

class DataCleaner:
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """Main entry point for data cleaning pipeline."""
        if df.empty:
            return df
        
        df = DataCleaner.normalize_columns(df)
        df = DataCleaner.handle_missing_values(df)
        df = DataCleaner.flatten_nested_data(df)
        return df

    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Converts headers to clean_snake_case (fixes the user__i_d bug)."""
        def to_snake_case(name):
            # 1. Replace spaces/hyphens with underscores immediately
            name = re.sub(r'[\s\-]+', '_', str(name))
            # 2. Handle camelCase/PascalCase (e.g., UserID -> User_ID)
            name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
            # 3. Strip any remaining non-alphanumeric junk
            name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
            # 4. Collapse multiple underscores and lowercase
            return re.sub(r'_+', '_', name).lower().strip('_')

        df.columns = [to_snake_case(col) for col in df.columns]
        return df

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes missing values to None for clean JSON output."""
        return df.where(pd.notnull(df), None)

    @staticmethod
    def flatten_nested_data(df: pd.DataFrame) -> pd.DataFrame:
        """Explodes nested dictionaries into separate columns."""
        for col in df.columns:
            if df[col].dropna().empty:
                continue
            
            sample = df[col].dropna().iloc[0]
            if isinstance(sample, dict):
                # FIX: Convert Series to list and align index
                flattened = pd.json_normalize(df[col].tolist())
                flattened.index = df.index  # Keep row alignment
                
                flattened.columns = [f"{col}_{subcol}" for subcol in flattened.columns]
                df = df.drop(columns=[col]).join(flattened)
        return df