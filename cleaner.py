import pandas as pd


class CSVDataCleanerAgent:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def remove_nulls(self):
        before = len(self.df)
        self.df.dropna(inplace=True)
        return f"Removed {before - len(self.df)} null rows"

    def drop_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        return f"Removed {before - len(self.df)} duplicates"

    def show_head(self):
        return self.df.head().to_dict()

    def get_info(self):
        return {
            "columns": list(self.df.columns),
            "shape": self.df.shape
        }
