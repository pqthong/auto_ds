import streamlit as st
import pandas as pd
import requests
import io
import ast
import re
import matplotlib.pyplot as plt
import seaborn as sns

def handle_file_upload(uploaded_files):
    dataframes = []
    files = {}
    
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        dataframes.append(df)

        st.write(f"### Original Data Preview ({uploaded_file.name})")
        st.dataframe(df)

        data = uploaded_file.getvalue()
        files[uploaded_file.name] = (uploaded_file.name, data, uploaded_file.type)

    st.info("Processing data. Please wait...")
    url = "http://backend:5000/upload/"
    response = requests.post(url, files=files)

    if response.status_code == 200:
        st.session_state.upload_result = response.json()

    if st.session_state.upload_result:
        result = st.session_state.upload_result

        cleaned_data = pd.read_csv(io.StringIO(result["cleaned_data"]))
        st.write("### Cleaned Data Preview")
        st.dataframe(cleaned_data)

        return dataframes, cleaned_data, result
    return None, None, None


def display_generated_graphs(cleaned_data, result):
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
                pass
    for idx, fig in enumerate(st.session_state.generated_graphs):
        st.write(f"#### Graph {idx + 1}")
        st.pyplot(fig)
