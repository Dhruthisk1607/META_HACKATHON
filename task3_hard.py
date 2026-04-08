def grader(state):
    nulls = sum(state.get("null_values", {}).values())
    dups = state.get("duplicates", 0)
    score = 1.0 if nulls == 0 and dups == 0 else max(0.0, 1.0 - (nulls + dups)/20)
    return {
        "score": score,
        "feedback": "Excellent cleaning!" if score == 1.0 else "Still some issues"
    }