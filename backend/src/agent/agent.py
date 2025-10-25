from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
from asi1 import asi1
from tools import TOOLS_FORMATTED, TOOLS_DICT
from prompts import AGENT_PROMPT, SUMMARY_PROMPT
import json
from metta import metta
from dashboard import dashboard

from operator import add as add_messages
from typing import List, Annotated, TypedDict, Any
import ftfy

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

def tool_node(state: AgentState):
    
    results = []
    func = state["messages"][-1]["tool_calls"][0]
    args = json.loads(func["function"]["arguments"])
    args = {k: v for k, v in args.items() if v is not None}
    print("calling tool: " + func["function"]["name"] + " with args: " + json.dumps(args))
    result = TOOLS_DICT[func["function"]["name"]](**args)
    results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": func["id"],})
    return {"messages": results }


def has_tools(state: AgentState):
    """ Conditional edge. """
    if state["messages"][-1].get("tool_calls", None):
        return True
    return False


def create_dashboard(state: AgentState):
    state["messages"][-1]["content"] = "SUMMARY: " + state["messages"][-1]["content"].message.content
    print(json.dumps(state["messages"], indent=2))
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

    final_dashboard = {}
    final_dashboard["summary"] = cleaned_summary

    for i, message in enumerate(state["messages"]):
        if message["role"] == "tool":
            func = state["messages"][i - 1]["tool_calls"][0]["function"]
            args = json.loads(func["arguments"])
            data = json.loads(message["content"])
            match func["name"]:
                case "historical_data":
                    dashboard.create_graph(data, args)
                case "coin_general_data":
                    dashboard.create_table(data, args)
                case "fear_and_greed_index":
                    dashboard.create_radial(data, args, "Fear and Greed")
                case "social_sentiment_tool":
                    dashboard.create_radial(data, args, "Social Sentiment")
                case "web_search":
                    print("here")
                    dashboard.create_recomended(data)
                case _:
                    print(f"no relevant dashboard component for {func}.")

    dashboard.finalize_table()
    dashboard.finalize_recommended()
    dashboard.add_summary(cleaned_summary)
    dashboard.sort_dashboard()

    #print(json.dumps(dashboard.final_dashboard))
    return {
        "messages": [
            dashboard.final_dashboard
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

def run_agent(prompt: str) -> List:

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
    result = agent.invoke({"messages": input})

    return result["messages"][-1]
