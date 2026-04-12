import pandas as pd


class CSVDataCleanerAgent:
    def __init__(self, file_path):
        self.original_df = pd.read_csv(file_path)
        self.df = self.original_df.copy()

    def reset(self):
        self.df = self.original_df.copy()
        return "Reset complete"

    def remove_nulls(self):
        before = len(self.df)
        self.df = self.df.dropna()
        removed = before - len(self.df)
        return {"removed_null_rows": removed}

    def drop_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = before - len(self.df)
        return {"removed_duplicates": removed}

    def show_head(self):
        return self.df.head().to_dict(orient="records")

    def get_info(self):
        return {
            "columns": list(self.df.columns),
            "shape": list(self.df.shape)
        }
