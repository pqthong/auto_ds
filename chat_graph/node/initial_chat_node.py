from typing import Dict, List
from langchain_core.messages import AIMessage
from chat_graph.state import ChatState
from react_agent.utils import load_chat_model
from react_agent.configuration import Configuration
from chat_graph.prompts import basic
from langchain_core.runnables import RunnableConfig

async def basic_chat(state: ChatState, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    """Generates a detailed statistical summary of the dataset using LLM."""

    # Load model
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    # Craft a prompt for LLM
    prompt = basic()

    # Call the LLM to generate advanced insights
    response = await model.ainvoke([
        {"role": "system", "content": prompt},
        *state.messages,
    ], config)

    # Update state with the statistical summary and insights
    code_str = response.content
    return {"messages": [response]}
