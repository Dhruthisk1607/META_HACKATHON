import gradio as gr
import pandas as pd
from environment import CSVCleanerEnvironment

def run_cleaner(file):
    # Load CSV
    df = pd.read_csv(file.name)

    # Initialize environment
    env = CSVCleanerEnvironment()

    # Start process
    env.reset()
    
    # Example step loop (adjust based on your logic)
    done = False
    state = None

    while not done:
        action = env.cleaner.act(state)
        state, reward, done, info = env.step(action)

    # Assuming final cleaned dataframe stored
    cleaned_df = env.cleaner.dataframe

    return cleaned_df

interface = gr.Interface(
    fn=run_cleaner,
    inputs=gr.File(label="Upload CSV"),
    outputs="dataframe",
    title="CSV Cleaner Agent"
)

interface.launch()