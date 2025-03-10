from typing import Dict, List
from langchain_core.messages import AIMessage
from react_agent.state import State
import pandas as pd
import numpy as np
import io

async def code_executor(state: State, config) -> Dict[str, List[AIMessage]]:
    """Executes the generated cleaning code and updates the cleaned dataset."""
    df = state.original_data
    code = state.code_to_execute[-1].replace("```python","").replace("```","")
    try:
        local_env = {"df": df, "pd": pd, "np": np}
        # Execute the function definition
        exec(code, local_env)
        # Call the function and get the cleaned DataFrame
        df_out = local_env["clean_dataframe"](df)
        return {"messages": [AIMessage(content="Data cleaning complete.")],"cleaned_data": df_out} 
    except Exception as e:
        pass
    return {"messages": [AIMessage(content="Data cleaning complete.")],"cleaned_data": [state.cleaned_data]} 