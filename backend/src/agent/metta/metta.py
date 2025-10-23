from hyperon import MeTTa, ValueAtom, E, S
import os
from pydantic import BaseModel
from openai import pydantic_function_tool
from asi1 import asi1

metta = MeTTa()

def initialize_knowledge_graph():

    # Type, tone, category -> summary prompt
    metta.space().add_atom(E(S("data"), S("professional"), S("general"), ValueAtom("Summarize professionally, focusing on market trends, prices, volume, and ecosystem implications.")))
    metta.space().add_atom(E(S("data"), S("casual"), S("general"), ValueAtom("Give an easy-to-understand overview of market trends, coin prices, and important news for beginners.")))
    metta.space().add_atom(E(S("data"), S("professional"), S("numerical"), ValueAtom("Provide detailed numerical analysis of prices, volumes, market cap, and historical trends.")))
    metta.space().add_atom(E(S("data"), S("casual"), S("numerical"), ValueAtom("Show the key numbers like price, volume, and market cap in a simple and understandable way.")))
    metta.space().add_atom(E(S("data"), S("casual"), S("textual"), ValueAtom("Write a simple, narrative explanation of what the data shows and why it matters.")))

    metta.space().add_atom(E(S("advice"), S("professional"), S("general"), ValueAtom("Provide strategic advice based on aggregated data, including risk assessment and technical considerations.")))
    metta.space().add_atom(E(S("advice"), S("casual"), S("general"), ValueAtom("Give friendly, easy-to-understand guidance on what actions to consider based on overall trends.")))
    metta.space().add_atom(E(S("advice"), S("professional"), S("numerical"), ValueAtom("Offer advice based on quantitative metrics, historical data, and calculated risks.")))
    metta.space().add_atom(E(S("advice"), S("casual"), S("numerical"), ValueAtom("Give simple, number-based guidance on this coin or metric, easy to follow and practical.")))
    metta.space().add_atom(E(S("advice"), S("casual"), S("textual"), ValueAtom("Give easy-to-read, friendly advice in text form, explaining what steps to take and why.")))

    metta.space().add_atom(E(S("news"), S("professional"), S("general"), ValueAtom("Summarize recent news and sentiment trends in a formal, analytical style focusing on market implications.")))
    metta.space().add_atom(E(S("news"), S("casual"), S("general"), ValueAtom("Give a simple overview of what's happening in crypto, including social sentiment and important headlines.")))
    metta.space().add_atom(E(S("news"), S("professional"), S("numerical"), ValueAtom("Provide professional summaries of market data, price changes, and social sentiment metrics.")))
    metta.space().add_atom(E(S("news"), S("casual"), S("numerical"), ValueAtom("Explain the latest numbers and trends for this coin in a simple, easy-to-understand way.")))
    metta.space().add_atom(E(S("news"), S("casual"), S("textual"), ValueAtom("Write a casual summary of the latest news and trends, easy for beginners to understand.")))

    if not os.path.exists("knowledge.metta"):
        with open("knowledge.metta", "w") as _: pass
    else:
        with open("knowledge.metta", "r") as file:
            try:
                for line in file.readlines():
                    metta.run(line.strip())
            except Exception:
                pass

def add_to_knowlegde_graph(type: str, tone: str, category: str, prompt: str):
    
    # Simple cache.
    atom = E(S(type), S(tone), S(category), ValueAtom(prompt))
    metta.space().add_atom(atom)
    with open("knowledge.metta", "a") as file:
        file.write(str(atom))

def generate_new_atom(type: str, tone: str, category: str):

    class Prompt(BaseModel):
        prompt: str

    response = asi1.asi_request(
        [
            {
                "role": "system",
                "content": f"Given  the extracted parameters type:{type} tone:{tone} and category:{category}. Give a single sentence prompt for an LLM to summarize a request of this type in relation to crypto/web3. Return nothing else."
            },
        ],
        tools=[pydantic_function_tool(Prompt, name="prompt")],
        using_structured_output=True
    )
    
    add_to_knowlegde_graph(type, tone, category, asi1.get_structured_output(response)["prompt"])

def extract_type_tone_category(query):
    
    class Params(BaseModel):
        type: str
        tone: str
        category: str

    response = asi1.asi_request(
        [
            {
                "role": "system",
                "content": f"Given the query: {query}, extract three parameters. Type: the type of request. Must be 'data', 'advice', or 'news'. Tone: the tone of the request. Must be 'casual' or 'professional'. Category: the category of the request. Some examples are 'general', 'numerical, and 'textual'. Make sure to be specific to the tone, category, and type."
            },
        ],
        tools=[pydantic_function_tool(Params, name="params")],
        using_structured_output=True
    )

    return asi1.get_structured_output(response)

def get_prompt(type_: str, tone: str, category: str):

    type_ = type_.strip()
    tone = tone.strip()
    category = category.strip()

    result = metta.run(f"! (match &self ({type_} {tone} {category} $x) $x)")
    result = [r[0].get_object().value for r in result if r and len(r) > 0] #type: ignore

    if not result:
        generate_new_atom(type_, tone, category)
    else:
        return result
    
    return get_prompt(type_, tone, category)

initialize_knowledge_graph()

