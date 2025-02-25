from typing import Dict, List
from langchain_core.messages import AIMessage
from chat_graph.state import ChatState
import pandas as pd
import numpy as np
import io
from chat_graph.prompts import answer
from react_agent.utils import load_chat_model
from react_agent.configuration import Configuration

async def pandas_exec(state: ChatState, config) -> Dict[str, List[AIMessage]]:
    """Executes the generated cleaning code and updates the cleaned dataset."""
    df = state.df
    summary = df.describe(include='all').to_string()
    code = state.code[-1].replace("```python","").replace("```","")
    print(f'Code to execute: {code}')
    try:
        local_env = {"df": df, "pd": pd, "np": np}
        # Execute the function definition
        exec(code, local_env)
        # Call the function and get the cleaned DataFrame
        df_out = local_env["process_df"](df)
        configuration = Configuration.from_runnable_config(config)
        model = load_chat_model(configuration.model)
        # Craft a prompt for LLM
        prompt = answer()

        # Create a single message for the LLM
        message = f"""
        query: {state.messages[-1].content}
        
        Hint: {df_out}

        Dataset Columns: {list(df.columns)}

        Statistical Summary:
        {summary}

        Sample Data: {df.head(15).to_dict(orient='records')}
        """

        # Call the LLM to generate advanced insights
        response = await model.ainvoke([
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ], config)
        print(f'res: {response.content}')
        return {"messages": [response]}

    except Exception as e:
        print(f"Error executing code: {e}")

    return {"messages": [AIMessage(content="Data cleaning complete.")]} 