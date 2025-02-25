from typing import Dict, List
from langchain_core.messages import AIMessage
from chat_graph.state import ChatState
from react_agent.utils import load_chat_model
from react_agent.configuration import Configuration
from chat_graph.prompts import basic
from langchain_core.runnables import RunnableConfig

async def pd_gen_chat(state: ChatState, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generates a detailed statistical summary of the dataset using LLM."""

    df = state.df
    print(f'Starting statistical analysis on data: {df.head(2)}')
    # Generate basic statistical summary
    summary = df.describe(include='all').to_string()

    message = f"""
    {state.messages[-1].content}

    Dataset Columns: {list(df.columns)}

    Statistical Summary:
    {summary}

    Sample Data: {df.head(15).to_dict(orient='records')}
    """

    # Load model
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    # Craft a prompt for LLM
    prompt = basic()

    # Call the LLM to generate advanced insights
    response = await model.ainvoke([
        {"role": "system", "content": prompt},
        {"role": "user", "content": message},
    ], config)

    # Update state with the statistical summary and insights
    return {"code": [response.content]}
