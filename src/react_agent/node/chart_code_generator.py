from typing import Dict, List
from langchain_core.messages import AIMessage
from react_agent.state import State
from react_agent.configuration import RunnableConfig
from langchain_core.runnables import RunnableConfig
from react_agent.utils import load_chat_model
from react_agent.prompts import get_chart_generate_promt
from react_agent.configuration import Configuration




async def chart_code_generator(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generates a detailed statistical summary of the dataset using LLM."""
    df = state.cleaned_data
    summary = df.describe(include='all').to_string()

    # Load model
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    # Craft a prompt for LLM
    prompt = get_chart_generate_promt()

    # Create a single message for the LLM
    message = f"""
    Analyze the dataset and provide code for visualization.

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

    # Update state with the statistical summary and insights
    code_str = response.content
    return {"messages": [response],"graphs_code": [code_str]}