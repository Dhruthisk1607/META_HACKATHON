from fastapi import FastAPI
import pandas as pd
from cleaner import CSVDataCleanerAgent

app = FastAPI()

cleaner = None


@app.get("/")
def home():
    return {"message": "CSV Cleaner API running"}


@app.post("/reset")
def reset():
    global cleaner
    cleaner = CSVDataCleanerAgent("messy_data.csv")
    return {"status": "reset done"}


@app.post("/step")
def step(action: dict):
    global cleaner

    if action["action_type"] == "show_head":
        return cleaner.show_head()

    if action["action_type"] == "remove_nulls":
        return cleaner.remove_nulls()

    if action["action_type"] == "drop_duplicates":
        return cleaner.drop_duplicates()

    if action["action_type"] == "get_info":
        return cleaner.get_info()

    return {"error": "invalid action"}
