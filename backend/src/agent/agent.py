from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END, START

from dotenv import load_dotenv
from openai import OpenAI
import os

from operator import add as add_messages
from typing import List, Annotated, TypedDict

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

def asi_request(messages: List, model: str = "asi1-extended", temperature: float = 0.1, max_tokens: int = 2000):

    client = OpenAI(
        api_key=os.getenv("ASIONE_KEY"),
        base_url="https://api.asi1.ai/v1"
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response

def initial_request(state: AgentState):
    pass
