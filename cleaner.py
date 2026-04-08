import pandas as pd

class CSVDataCleanerAgent:
    def __init__(self, file_path=None):
        self.actions_taken = []

        if file_path:
            self.df = pd.read_csv(file_path)
        else:
            self.df = None

    # ✅ For Hugging Face
    def clean(self, df):
        self.df = df.copy()
        self.df = self.df.drop_duplicates()
        self.df = self.df.fillna(0)
        return self.df

    # ✅ For OpenEnv
    def take_action(self, action: str):
        action = action.lower().strip()
        self.actions_taken.append(action)

        if action == "drop nulls":
            self.df = self.df.dropna()

        elif action == "fill nulls":
            self.df = self.df.fillna(0)

        elif action == "remove duplicates":
            self.df = self.df.drop_duplicates()

        elif action.startswith("strip column"):
            col = action.replace("strip column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()

        elif action.startswith("lowercase column"):
            col = action.replace("lowercase column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.lower()

        elif action.startswith("fill with mean column"):
            col = action.replace("fill with mean column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].mean())

        elif action.startswith("fill with median column"):
            col = action.replace("fill with median column", "").strip()
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].median())

        elif action.startswith("drop column"):
            col = action.replace("drop column", "").strip()
            if col in self.df.columns:
                self.df = self.df.drop(columns=[col])

        else:
            raise ValueError(f"Unknown action: {action}")

    def get_state(self):
        return {
            "rows": len(self.df),
            "columns": list(self.df.columns),
            "null_values": self.df.isnull().sum().to_dict(),
            "duplicates": self.df.duplicated().sum(),
            "actions_taken": self.actions_taken
        }

    def is_clean(self):
        return self.df.isnull().sum().sum() == 0 and self.df.duplicated().sum() == 0
