from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from openai import OpenAI
import os

from operator import add as add_messages
from typing import List, Annotated, TypedDict, Any

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

def asi_request(messages: List, model: str = "asi1-extended", temperature: float = 0.1, max_tokens: int = 2000, tools: Any | None = None, using_structured_output: bool = False):

    client = OpenAI(
        api_key=os.getenv("ASIONE_KEY"),
        base_url="https://api.asi1.ai/v1",
    )

    if using_structured_output:
        response = client.beta.chat.completions.parse(
            model="asi1-experimental",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools or [],
        )
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools or [],
        )
    
    return response

def llm(state: AgentState):
    pass

def tool_node(state: AgentState):
    pass

def create_dashboard(state: AgentState):
    pass
