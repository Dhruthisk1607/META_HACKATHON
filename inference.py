import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")


def predict():
    print("[START] Inference started")

    # =========================
    # RESET EPISODE
    # =========================
    print("[STEP] Calling reset")

    reset_response = requests.post(f"{API_BASE_URL}/reset")
    reset_data = reset_response.json()

    print("[STEP] Reset successful")

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

        print(f"[STEP] Executing action: {action['action_type']}")

        response = requests.post(
            f"{API_BASE_URL}/step",
            json=action
        )

        data = response.json()

        obs = data["observation"]
        done = data["done"]

        print(f"[STEP] Result: {obs['status']}")

    # =========================
    # END
    # =========================
    print("[END] Inference completed")

    return {
        "observation": obs,
        "done": done
    }


# =========================
# LOCAL TEST
# =========================
if __name__ == "__main__":
    result = predict()
    print(result)
