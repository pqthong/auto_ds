
from typing import Dict, List, cast
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model
from react_agent.configuration import Configuration
from react_agent.state import State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model
from react_agent.prompts import get_data_cleaning_prompt
import pandas as pd
import numpy as np
import json
import io
from react_agent.prompts import get_data_cleaning_prompt
async def data_cleaner(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    df = state.original_data
    message = f"Dataset Columns: {list(df.columns)}"
    state.messages.append(message)  # Store the message in DataState

    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)


    response = await model.ainvoke([
        {"role": "system", "content": get_data_cleaning_prompt()},
        {"role": "user", "content": message},
        {"role": "user", "content": f"Sample Data: {df.head(5).to_dict(orient='records')}"}
    ], config)
    return {"messages": [response], "code_to_execute": [response.content]}

 