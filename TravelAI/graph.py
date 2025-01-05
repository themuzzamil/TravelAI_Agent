from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from TravelAI.tools import llm_tool, tool
from TravelAI.prompt import prompt


def output(state: MessagesState):
  system_msg = prompt.format()
  return {"messages": [llm_tool.invoke([SystemMessage(content=system_msg)]+state["messages"])]}




memory = MemorySaver()
builder = StateGraph(MessagesState)

builder.add_node("Chatbot",output)
builder.add_node("tools",ToolNode(tool))

builder.add_edge(START,"Chatbot")
builder.add_conditional_edges(
    "Chatbot",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "Chatbot")

graph = builder.compile(checkpointer=memory)
