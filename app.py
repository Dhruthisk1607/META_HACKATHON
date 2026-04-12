import gradio as gr
from cleaner import CSVDataCleanerAgent

# initialize agent once (important)
agent = CSVDataCleanerAgent("messy_data.csv")


def run_action(action):
    try:
        action = action.strip().lower()

        if action == "remove_nulls":
            return {
                "result": agent.remove_nulls()
            }

        elif action == "drop_duplicates":
            return {
                "result": agent.drop_duplicates()
            }

        elif action == "show_head":
            return {
                "result": agent.show_head()
            }

        elif action == "get_info":
            return {
                "result": agent.get_info()
            }

        else:
            return {
                "error": "Invalid action. Use: remove_nulls, drop_duplicates, show_head, get_info"
            }

    except Exception as e:
        return {"error": str(e)}


demo = gr.Interface(
    fn=run_action,
    inputs="text",
    outputs="json",
    title="CSV Cleaner Agent",
    description="Actions: remove_nulls, drop_duplicates, show_head, get_info"
)

demo.launch()
