import uuid
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# ------------------------
# FASTAPI APP
# ------------------------
app = FastAPI()

# ------------------------
# GLOBAL STATE
# ------------------------
env_state = {
    "df": None,
    "episode_id": "",
    "step_count": 0
}

# ------------------------
# MODELS
# ------------------------
class Action(BaseModel):
    action_type: str
    parameters: dict = {}

# ------------------------
# RESET
# ------------------------
@app.post("/reset")
def reset():
    try:
        df = pd.read_csv("messy_data.csv")

        env_state["df"] = df
        env_state["episode_id"] = str(uuid.uuid4())
        env_state["step_count"] = 0

        return {
            "observation": {
                "status": "success",
                "data": "Environment reset successful"
            },
            "reward": 0,
            "done": False
        }

    except Exception as e:
        return {
            "observation": {
                "status": "error",
                "data": str(e)
            },
            "reward": 0,
            "done": True
        }

# ------------------------
# STEP
# ------------------------
@app.post("/step")
def step(action: Action):
    try:
        df = env_state["df"]

        if df is None:
            return {
                "observation": {
                    "status": "error",
                    "data": "Environment not initialized. Call /reset first."
                },
                "reward": 0,
                "done": True
            }

        action_type = action.action_type

        # ---------------- ACTIONS ----------------

        if action_type == "show_head":
            data = df.head().to_dict()

        elif action_type == "remove_nulls":
            before = len(df)
            df = df.dropna()
            env_state["df"] = df
            data = f"Removed {before - len(df)} null rows"

        elif action_type == "drop_duplicates":
            before = len(df)
            df = df.drop_duplicates()
            env_state["df"] = df
            data = f"Removed {before - len(df)} duplicates"

        elif action_type == "get_info":
            data = str(df.info())

        else:
            return {
                "observation": {
                    "status": "error",
                    "data": f"Unknown action: {action_type}"
                },
                "reward": 0,
                "done": True
            }

        env_state["step_count"] += 1

        return {
            "observation": {
                "status": "success",
                "data": data
            },
            "reward": 1,
            "done": False
        }

    except Exception as e:
        return {
            "observation": {
                "status": "error",
                "data": str(e)
            },
            "reward": 0,
            "done": True
        }

# ------------------------
# STATE
# ------------------------
@app.get("/state")
def state():
    return {
        "episode_id": env_state["episode_id"],
        "step_count": env_state["step_count"]
    }

# ------------------------
# ROOT (IMPORTANT FOR HF)
# ------------------------
@app.get("/")
def home():
    return {"message": "CSV Cleaner API is running"}
