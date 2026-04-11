from fastapi import FastAPI
import uuid

from cleaner import CSVDataCleanerAgent
from models import CleanerAction

app = FastAPI()

cleaner = None
step_count = 0
episode_id = ""



@app.post("/reset")
def reset():
    global cleaner, step_count, episode_id

    step_count = 0
    episode_id = str(uuid.uuid4())

    cleaner = CSVDataCleanerAgent("messy_data.csv")

    return {
        "observation": {
            "status": "ready",
            "episode_id": episode_id,
            "message": "Environment reset successful"
        },
        "done": False
    }



@app.post("/step")
def step(action: CleanerAction):
    global cleaner, step_count

    step_count += 1

    try:
        if action.action_type == "remove_nulls":
            result = cleaner.remove_nulls()

        elif action.action_type == "drop_duplicates":
            result = cleaner.drop_duplicates()

        elif action.action_type == "show_head":
            result = cleaner.show_head()

        elif action.action_type == "get_info":
            result = cleaner.get_info()

        else:
            result = f"Unknown action: {action.action_type}"

        return {
            "observation": {
                "status": "success",
                "data": result
            },
            "reward": 1.0,
            "done": False
        }

    except Exception as e:
        return {
            "observation": {
                "status": "error",
                "data": str(e)
            },
            "reward": 0.0,
            "done": True
        }



@app.get("/")
def home():
    return {"message": "CSV Cleaner API is running"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
