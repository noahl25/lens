from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from .asi1 import asi1
from .tools import TOOLS_FORMATTED, TOOLS_DICT
from .prompts import AGENT_PROMPT, SUMMARY_PROMPT
import json
from .metta import metta
from .dashboard import dashboard

from operator import add as add_messages
from typing import List, Annotated, TypedDict, Any
import ftfy
import asyncio

from uagents_adapter import LangchainRegisterTool, cleanup_uagent

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

def stringify_content(c): 
    c["content"] = str(c["content"])
    return c

def llm(state: AgentState):

    response = asi1.asi_request_with_retry(
        [message for message in state["messages"]],
        tools=TOOLS_FORMATTED
    )

    print(json.dumps(state["messages"], indent=2))

    if response.choices[0].message.tool_calls:
        tool = response.choices[0].message.tool_calls[0]
        return {
            "messages": [
                {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": tool.id,
                            "type": "function",
                            "index": str(len(state["messages"]) - 1),
                            "function": {
                                "name": tool.function.name, #type: ignore
                                "arguments": tool.function.arguments, #type: ignore
                            }
                        }
                    ]
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": response.choices[0]
                }
            ]
        }

async def tool_node(state: AgentState):
    
    results = []
    func = state["messages"][-1]["tool_calls"][0]
    args = json.loads(func["function"]["arguments"])
    args = {k: v for k, v in args.items() if v is not None}
    print("calling tool: " + func["function"]["name"] + " with args: " + json.dumps(args))
    tool_func = TOOLS_DICT[func["function"]["name"]]
    if asyncio.iscoroutinefunction(tool_func):
        result = await tool_func(**args)
    else:
        result = tool_func(**args)
    results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": func["id"],})
    return {"messages": results }


def has_tools(state: AgentState):
    """ Conditional edge. """
    if state["messages"][-1].get("tool_calls", None):
        return True
    return False


def create_dashboard(state: AgentState):
    state["messages"][-1]["content"] = state["messages"][-1]["content"].message.content
    # print(json.dumps(state["messages"], indent=2))
    cleaned_summary = ftfy.fix_encoding(state["messages"][-1]["content"])
    response = asi1.asi_request(
        [
            {
                "role": "system",
                "content": "Extract the summary from the following query. Use plaintext and professional language. Keep as much information as possible."
            },
            {
                "role": "user",
                "content": cleaned_summary
            }
        ]
    ) # In case the model hallucinates initially.
    cleaned_summary = ftfy.fix_encoding(response.choices[0].message.content) #type: ignore

    dash = dashboard.DashboardBuilder()

    for i, message in enumerate(state["messages"]):
        if message["role"] == "tool":
            func = state["messages"][i - 1]["tool_calls"][0]["function"]
            args = json.loads(func["arguments"])
            data = json.loads(message["content"])
            match func["name"]:
                case "historical_data":
                    dash.create_graph(data, args)
                case "coin_general_data":
                    dash.create_table(data, args)
                case "fear_and_greed_index":
                    dash.create_radial(data, args, "Fear and Greed")
                case "social_sentiment_tool":
                    dash.create_radial(data, args, "Social Sentiment")
                case "web_search":
                    dash.create_recomended(data)
                case _:
                    print(f"no relevant dashboard component for {func}.")

    dash.finalize_table()
    dash.finalize_recommended()
    dash.add_summary(cleaned_summary)
    dash.sort_dashboard()

    #print(json.dumps(dashboard.final_dashboard))
    return {
        "messages": [
            dash.get_final_dashboard()
        ]
    }
    

graph = StateGraph(AgentState)
def create_agent():
    graph.add_node("llm", llm)
    graph.add_node("tool_node", tool_node)
    graph.add_node("create_dashboard", create_dashboard)

    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", has_tools, {
        True: "tool_node",
        False: "create_dashboard"
    })
    graph.add_edge("tool_node", "llm")
    graph.add_edge("create_dashboard", END)
    
create_agent()

async def run_agent(prompt: str) -> List:

    vars = metta.extract_type_tone_category(prompt)
    metta_query = metta.get_prompt(vars["type"], vars["tone"], vars["category"])

    input = [
        {
            "role": "system",
            "content": AGENT_PROMPT + metta_query[0]
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    agent = graph.compile()
    result = await agent.ainvoke({"messages": input})

    return result["messages"][-1]

async def langgraph_agent(query):

    if isinstance(query, dict) and "input" in query:
        query = query["input"]
        
    result = await run_agent(query) #type: ignore

    return result

tool: Any = LangchainRegisterTool()
agent_info = tool.invoke(
    {
        "agent_obj": langgraph_agent,
        "name": "dashboard_agent",
        "port": 9000,
        "description": "A dashboard-generating LangGraph agent that fetches data and builds visual crypto insights.",
        "api_token": os.getenv("AGENTVERSE_KEY"),
        "mailbox": True,
    }
)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    cleanup_uagent("dashboard_agent")