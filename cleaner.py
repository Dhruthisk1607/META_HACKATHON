import pandas as pd

class CSVDataCleanerAgent:
    def __init__(self):
        self.df = None
        self.actions_taken = []

    def clean(self, df):
        """Simple automatic cleaning (safe for Hugging Face)"""
        self.df = df.copy()

        # Remove duplicates
        self.df = self.df.drop_duplicates()

        # Fill nulls with 0
        self.df = self.df.fillna(0)

        return self.df
