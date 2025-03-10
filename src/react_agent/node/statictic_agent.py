from typing import Dict, List
from langchain_core.messages import AIMessage
from react_agent.state import State
from react_agent.utils import load_chat_model
from react_agent.configuration import Configuration
from react_agent.prompts import get_static_analyzer_prompt
from langchain_core.runnables import RunnableConfig
from logger import logger  # Import the logger

async def statistical_analyzer(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    logger.info(f"Starting statistical analysis for state: {state}")  # Add logging
    df = state.cleaned_data

    # Generate basic statistical summary
    summary = df.describe(include='all').to_string()

    # Load model
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    # Craft a prompt for LLM
    prompt = get_static_analyzer_prompt()

    # Create a single message for the LLM
    message = f"""
    Analyze the dataset and provide advanced statistical insights.

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
    logger.info(f"Statistical analysis result: {response.content}")  # Add logging
    code_str = response.content
    return {"messages": [response], "code_to_execute": [response.content]}
