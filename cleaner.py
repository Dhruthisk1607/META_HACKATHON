import pandas as pd

class CSVDataCleanerAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)   
        self.history = []

class CSVDataCleanerAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.history = []

    def take_action(self, action: str):
        action = action.lower().strip()
        self.history.append(action)

        if action == "drop nulls":
            self.df.dropna(inplace=True)

        elif action == "fill nulls":
            self.df.ffill(inplace=True)

        elif action == "remove duplicates":
            self.df.drop_duplicates(inplace=True)

        elif action.startswith("strip column"):
            col = action.replace("strip column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()

        elif action.startswith("lowercase column"):
            col = action.replace("lowercase column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.lower()

        else:
            print(f"Unknown action: {action}")

    def is_clean(self):
        no_nulls = not self.df.isnull().values.any()
        no_duplicates = not self.df.duplicated().any()
        return no_nulls and no_duplicates

    def get_state(self):
        return {
            "rows": len(self.df),
            "columns": list(self.df.columns),
            "null_values": self.df.isnull().sum().to_dict(),
            "duplicates": int(self.df.duplicated().sum())
        }

    def save(self, output_path):
        self.df.to_csv(output_path, index=False)
