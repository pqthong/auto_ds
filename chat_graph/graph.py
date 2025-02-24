"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime, timezone
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from react_agent.configuration import Configuration
from chat_graph.state import  ChatState
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model
from chat_graph.node.initial_chat_node import basic_chat
# Define the function that calls the model
from langgraph.checkpoint.memory import MemorySaver



builder = StateGraph(ChatState, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(basic_chat)


builder.add_edge("__start__", "basic_chat")
builder.add_edge(
    "basic_chat",
    "__end__"
)

# Add a normal edge from `tools` to `call_model`
# This creates a cycle: after using tools, we always return to the model

# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates

chat_graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[]
)
chat_graph.name = "Chat Agent"  # This customizes the name in LangSmith
