from typing import Dict, List, Any
from langchain_core.messages import AIMessage
from react_agent.state import State
import pandas as pd
import numpy as np
import io

async def statictic_code_executor(state: State, config) -> Dict[str, List[AIMessage]]:
    """Executes the generated cleaning code and updates the cleaned dataset."""
    df = state.cleaned_data
    code = state.code_to_execute[-1].replace("```python","").replace("```","")
    print(f'Code to execute: {code}')
    try:
        local_env = {"df": df, "pd": pd, "np": np, "Dict": Dict, "Any": Any}
        # Execute the function definition
        exec(code, local_env)
        # Call the function and get the cleaned DataFrame
        json_out = local_env["generate_statistical_summary"](df)
        print(f'json_out: {json_out}')
        return {"messages": [AIMessage(content="Data statictic calculate complete.")],"statistical_summary": json_out} 
    except Exception as e:
        print(f"Error executing code: {e}")
    return {"messages": [AIMessage(content="Data statictic calculate complete.")]} 