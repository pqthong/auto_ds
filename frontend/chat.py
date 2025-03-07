import streamlit as st
import pandas as pd
import requests
import json
import io
import matplotlib.pyplot as plt
import seaborn as sns
import re

def handle_chat(user_input, cleaned_data):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)
    if st.session_state.upload_result:
        data_json = cleaned_data.to_json(orient="records")

        chat_url = "http://backend:5000/chat/"
        chat_response = requests.post(chat_url, json={"query": user_input, "dataframe": data_json})

        if chat_response.status_code == 200:
            response_data = chat_response.json()
            assistant_message = response_data.get("answer", "I am analyzing your dataset...")
        else:
            assistant_message = "Error retrieving insights. Please try again."

        if "```json" in assistant_message:
            assistant_message = json.loads(assistant_message.replace("```json", "").replace("```", ""))
            visualizations = assistant_message.get("visualizations", [])
            assistant_message = assistant_message.get("answer", "I am analyzing your dataset...")
            graph = []
            for idx, code in enumerate(visualizations):
                try:
                    code = code.replace("```python", "").replace("```", "")
                    pattern = r"def\s+(\w+)\s*\("
                    match = re.search(pattern, code)
                    function_name = match.group(1)

                    local_env = {"df": cleaned_data, "plt": plt, "sns": sns, "pd": pd}
                    exec(code, local_env)
                    local_env[function_name](cleaned_data)
                    fig = plt.gcf()
                    graph.append(fig)
                except Exception as e:
                    pass
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.session_state.chat_responses.append(assistant_message)
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
            for idx, fig in enumerate(graph):
                st.pyplot(fig)
    else:
        assistant_message = "Upload some file first to get insights."
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
