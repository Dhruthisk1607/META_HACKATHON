def grader(state):
    nulls = sum(state.get("null_values", {}).values())
    score = 1.0 if nulls == 0 else max(0.0, 1.0 - nulls/50)
    return {
        "score": score,
        "feedback": "Perfect! No nulls left." if score == 1.0 else f"{nulls} nulls remaining"
    }