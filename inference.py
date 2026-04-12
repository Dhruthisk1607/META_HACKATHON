import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")


def predict():
    # =========================
    # RESET EPISODE
    # =========================
    reset_response = requests.post(f"{API_BASE_URL}/reset")
    reset_data = reset_response.json()

    done = False
    obs = None

    # =========================
    # ACTION SEQUENCE (TASKS)
    # =========================
    actions = [
        {"action_type": "show_head", "parameters": {}},
        {"action_type": "remove_nulls", "parameters": {}},
        {"action_type": "drop_duplicates", "parameters": {}},
        {"action_type": "get_info", "parameters": {}}
    ]

    # =========================
    # STEP LOOP
    # =========================
    for action in actions:
        if done:
            break

        response = requests.post(
            f"{API_BASE_URL}/step",
            json=action
        )

        data = response.json()

        obs = data["observation"]
        done = data["done"]

    # =========================
    # OUTPUT FORMAT (EVALUATOR SAFE)
    # =========================
    return {
        "observation": obs,
        "done": done
    }


# =========================
# OPTIONAL LOCAL TEST
# =========================
if __name__ == "__main__":
    result = predict()
    print(result)
