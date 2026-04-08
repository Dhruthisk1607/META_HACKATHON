import gradio as gr
import pandas as pd
from cleaner import CSVDataCleanerAgent

def run_cleaner(file):
    df = pd.read_csv(file.name)

    cleaner = CSVDataCleanerAgent()
    cleaned_df = cleaner.clean(df)

    return cleaned_df

interface = gr.Interface(
    fn=run_cleaner,
    inputs=gr.File(label="Upload CSV"),
    outputs="dataframe",
    title="CSV Cleaner Agent"
)

interface.launch()
