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
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model
from react_agent.node.clean_agent import data_cleaner
from react_agent.node.code_executor import code_executor
from react_agent.node.statictic_agent import statistical_analyzer
from react_agent.node.statictic_code_executor import statictic_code_executor
from react_agent.node.data_visualize import graph_suggest
from react_agent.node.chart_code_generator import chart_code_generator
from react_agent.node.insight import insight
from react_agent.node.sql_gen import sql_gen
# Define the function that calls the model
from langgraph.checkpoint.memory import MemorySaver



builder = StateGraph(State, config_schema=Configuration)

# Define the two nodes we will cycle between
builder.add_node(data_cleaner)
builder.add_node(code_executor)
builder.add_node(statistical_analyzer)
builder.add_node(statictic_code_executor)
builder.add_node(graph_suggest)
builder.add_node(chart_code_generator)
builder.add_node(insight)
builder.add_node(sql_gen)   

builder.add_edge("__start__", "data_cleaner")
builder.add_edge("data_cleaner", "code_executor")
builder.add_edge("code_executor", "statistical_analyzer")
builder.add_edge("statistical_analyzer", "statictic_code_executor")
builder.add_edge("statistical_analyzer", "graph_suggest")
builder.add_edge("graph_suggest", "chart_code_generator")
builder.add_edge("chart_code_generator", "insight")
builder.add_edge("insight", "sql_gen")
builder.add_edge(
    "sql_gen",
    "__end__"
)

# Add a normal edge from `tools` to `call_model`
# This creates a cycle: after using tools, we always return to the model

# Compile the builder into an executable graph
# You can customize this by adding interrupt points for state updates

graph = builder.compile(
    interrupt_before=[],  # Add node names here to update state before they're called
    interrupt_after=[]
)
graph.name = "ReAct Agent"  # This customizes the name in LangSmith
