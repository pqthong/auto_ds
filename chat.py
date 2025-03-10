import streamlit as st
import pandas as pd
import requests
import json
import io
import matplotlib.pyplot as plt
import seaborn as sns
import re
from chat_graph.graph import chat_graph
from chat_graph.state import ChatState
from langchain_core.runnables import RunnableConfig
import asyncio

async def get_chat_response(input, df):

    config = RunnableConfig(metadata={"message": "Starting chat."})
   
    result = await chat_graph.ainvoke(ChatState(
        messages=[input],
        df=df
    ), config=config)


    assistant_message = result["messages"][-1].content # Include generated graph code}
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

                local_env = {"df": df, "plt": plt, "sns": sns, "pd": pd}
                exec(code, local_env)
                local_env[function_name](df)
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



def handle_chat(user_input, cleaned_data):
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)
    if st.session_state.upload_result:
        asyncio.run(get_chat_response(user_input, cleaned_data))
        
    else:
        assistant_message = "Upload some file first to get insights."
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
