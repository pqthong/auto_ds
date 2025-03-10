import streamlit as st
import pandas as pd
import requests
import io
import ast
import re
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_core.runnables import RunnableConfig
from src.react_agent.graph import graph 
from chat_graph.graph import chat_graph
from src.react_agent.state import State
from logger import logger  # Import the logger

async def handle_file_upload(uploaded_file):
    logger.info(f"File uploaded: {uploaded_file.name}, Type: {uploaded_file.type}")  # Add logging
    
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write(f"### Original Data Preview ({uploaded_file.name})")
    st.dataframe(df)

    config = RunnableConfig(metadata={"message": "Starting data cleaning process."})

    # Run LangGraph Workflow
    result = await graph.ainvoke(State(
        original_data=df,
        messages=["Initial message: Data uploaded."]
    ), config=config)

    st.session_state.upload_result = result

    logger.info(f"File upload result: {result}")  # Add logging

    return result

def display_generated_graphs(cleaned_data, result):
    logger.info("Displaying generated graphs")  # Add logging
    st.write("### Generated Graphs")
    if not st.session_state.generated_graphs:
        graphs_code = result.get("graphs_code", [])[0].replace("```python", "").replace("```", "")
        graphs_code = ast.literal_eval(graphs_code)

        for idx, code in enumerate(graphs_code):
            try:
                code = code.replace("```python", "").replace("```", "")
                pattern = r"def\s+(\w+)\s*\("
                match = re.search(pattern, code)
                function_name = match.group(1)

                local_env = {"df": cleaned_data, "plt": plt, "sns": sns, "pd": pd}
                exec(code, local_env)
                local_env[function_name](cleaned_data)
                fig = plt.gcf()
                st.session_state.generated_graphs.append(fig)
            except Exception as e:
                logger.error(f"Error generating graph: {e}")  # Add logging
                pass
    for idx, fig in enumerate(st.session_state.generated_graphs):
        st.write(f"#### Graph {idx + 1}")
        st.pyplot(fig)
