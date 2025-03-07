import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import io
import json
import ast
import re
import sqlparse
from graphviz import Digraph

# Ensure session state is initialized
if "generated_graphs" not in st.session_state:
    st.session_state.generated_graphs = []

def parse_sql_to_erd(sql):
    statements = sqlparse.parse(sql)
    tables = {}
    relationships = []

    for stmt in statements:
        if stmt.get_type() == "CREATE":
            table_name = None
            columns = []

            for token in stmt.tokens:
                if token.ttype is None and token.get_real_name():
                    table_name = token.get_real_name()

                if isinstance(token, sqlparse.sql.Parenthesis):
                    col_defs = token.get_sublists()
                    for col_def in col_defs:
                        col_parts = [p.get_real_name() for p in col_def.get_sublists() if p.get_real_name()]
                        if col_parts:
                            columns.append(col_parts[0])

                        if "FOREIGN" in col_def.value:
                            ref_table = re.findall(r"REFERENCES\s+(\w+)", col_def.value)
                            if ref_table:
                                relationships.append((table_name, ref_table[0]))

            if table_name and columns:
                tables[table_name] = columns

    return tables, relationships

def generate_erd(sql):
    tables, relationships = parse_sql_to_erd(sql)

    dot = Digraph()

    for table, columns in tables.items():
        label = f"{{ {table} | " + " | ".join(columns) + " }}"
        dot.node(table, label=label, shape="record")

    for from_table, to_table in relationships:
        dot.edge(from_table, to_table, label="FK")

    return dot

st.set_page_config(page_title="Automated Data Science", layout="wide")

st.title("Automated Data Science")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "chat_responses" not in st.session_state:
    st.session_state.chat_responses = []

if "upload_result" not in st.session_state:
    st.session_state.upload_result = None

col1, col2 = st.columns([2, 2])

with col1:
    st.write("### Interactive Data Insights Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask about your dataset...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)
        if st.session_state.upload_result:
            cleaned_data = pd.read_csv(io.StringIO(st.session_state.upload_result["cleaned_data"]))
            data_json = cleaned_data.to_json(orient="records")

            chat_url = "http://backend:5000/chat/"
            chat_response = requests.post(chat_url, json={"query": user_input,
                                                          "dataframe": data_json
                                                          })

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
                        # Display cached graphs from session state
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

with col2:
    uploaded_file = st.file_uploader("Choose a file (CSV/Excel)", type=["csv", "xlsx"])

    if uploaded_file and not st.session_state.uploaded:
        st.session_state.uploaded = True

        st.subheader("Uploaded File Preview")

        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("### Original Data Preview")
        st.dataframe(df)

        st.info("Processing data. Please wait...")
        data = uploaded_file.getvalue()
        url = "http://backend:5000/upload/"
        files = {"file": (uploaded_file.name, data, "text/csv")}

        response = requests.post(url, files=files)

        if response.status_code == 200:
            st.session_state.upload_result = response.json()

    if st.session_state.upload_result:
        result = st.session_state.upload_result

        cleaned_data = pd.read_csv(io.StringIO(result["cleaned_data"]))
        st.write("### Cleaned Data Preview")
        st.dataframe(cleaned_data)

        st.write("### Entity Relationship Diagram (ERD)")
        erd = generate_erd(result["sql"].replace("```sql", "").replace("```", ""))
        st.graphviz_chart(erd)

        st.write("### Statistical Summary")
        st.write(result["statistical_summary"], expanded=False)

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
                    # Display cached graphs from session state
                except Exception as e:
                    pass
        for idx, fig in enumerate(st.session_state.generated_graphs):
            st.write(f"#### Graph {idx + 1}")
            st.pyplot(fig)
            

