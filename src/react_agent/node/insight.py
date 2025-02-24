from typing import Dict, List
from langchain_core.messages import AIMessage
from react_agent.state import State
from react_agent.utils import load_chat_model
from react_agent.configuration import Configuration
from react_agent.prompts import get_insight
from langchain_core.runnables import RunnableConfig



async def insight(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    df = state.cleaned_data
    summary = df.describe(include='all').to_string()
    
    # Load model
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)
    # Craft a prompt for LLM
    prompt = get_insight()

    # Create a single message for the LLM
    message = f"""
    Analyze the dataset and provide insight.

    Dataset Columns: {list(df.columns)}

    Statistical Summary:
    {summary}

    Data statistics:
    {state.statistical_summary}

    Sample Data: {df.head(15).to_dict(orient='records')}
    """

    # Call the LLM to generate advanced insights
    response = await model.ainvoke([
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ], config)
    print(f'res: {response.content}')
    return {"messages": [response], "insights": response.content}