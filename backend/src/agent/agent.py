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

    print(json.dumps(state, indent=2, default=str, ensure_ascii=False))
    state["messages"][-1]["content"] = "SUMMARY: " + state["messages"][-1]["content"].message.content
    cleaned_summary = state["messages"][-1]["content"].encode('utf-8').decode('unicode_escape').strip("[]").replace("â€$", "-").replace("â€", "-").replace("â", "-").replace("\\", "")
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
    cleaned_summary = response.choices[0].message.content.encode('utf-8').decode('unicode_escape').strip("[]").replace("â€$", "-").replace("â€", "-").replace("â", "-").replace("\\", "") #type: ignore

    #print(cleaned_summary)

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
                case _:
                    raise RuntimeError("No tool name match.")

    dashboard.finalize_table()

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

prompt = "bitcoin and ethereum metrics now"

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
agent.invoke({"messages": input})
