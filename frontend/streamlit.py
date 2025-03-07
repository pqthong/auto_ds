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
from utils import parse_sql_to_erd, generate_erd
from chat import handle_chat
from file_upload import handle_file_upload, display_generated_graphs

# Ensure session state is initialized
if "generated_graphs" not in st.session_state:
    st.session_state.generated_graphs = []

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
        handle_chat(user_input, pd.read_csv(io.StringIO(st.session_state.upload_result["cleaned_data"])))

with col2:
    uploaded_files = st.file_uploader("Choose files (CSV/Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        if st.button("Upload Files"):
            st.session_state.uploaded = True

            st.subheader("Uploaded File Preview")

            dataframes, cleaned_data, result = handle_file_upload(uploaded_files)

            if cleaned_data is not None:
                st.write("### Entity Relationship Diagram (ERD)")
                erd = generate_erd(result["sql"].replace("```sql", "").replace("```", ""))
                st.graphviz_chart(erd)

                st.write("### Statistical Summary")
                st.write(result["statistical_summary"], expanded=False)

                display_generated_graphs(cleaned_data, result)


