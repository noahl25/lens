from hyperon import MeTTa, ValueAtom, E, S
import os
 
metta = MeTTa()

def initialize_knowledge_graph():

    # Query type -> summary prompt
    metta.space().add_atom(E(S("data"), S("professional"), S("general"), ValueAtom("Summarize professionally, focusing on market trends, prices, volume, and ecosystem implications.")))
    metta.space().add_atom(E(S("data"), S("casual"), S("general"), ValueAtom("Give an easy-to-understand overview of market trends, coin prices, and important news for beginners.")))
    metta.space().add_atom(E(S("data"), S("professional"), S("specific"), ValueAtom("Provide a technical analysis of this specific data, including metrics, historical context, and implications.")))
    metta.space().add_atom(E(S("data"), S("casual"), S("specific"), ValueAtom("Explain the specific data simply, like you're describing it to a beginner.")))

    metta.space().add_atom(E(S("advice"), S("professional"), S("general"), ValueAtom("Provide strategic advice based on aggregated data, including risk assessment and technical considerations.")))
    metta.space().add_atom(E(S("advice"), S("casual"), S("general"), ValueAtom("Give friendly, easy-to-understand guidance on what actions to consider based on overall trends.")))
    metta.space().add_atom(E(S("advice"), S("professional"), S("specific"), ValueAtom("Offer specific, professional recommendations for this coin or metric, with reasoning.")))
    metta.space().add_atom(E(S("advice"), S("casual"), S("specific"), ValueAtom("Give simple advice for this coin or metric, easy to follow and practical.")))

    metta.space().add_atom(E(S("news"), S("professional"), S("general"), ValueAtom("Summarize recent news and sentiment trends in a formal, analytical style focusing on market implications.")))
    metta.space().add_atom(E(S("news"), S("casual"), S("general"), ValueAtom("Give a simple overview of what's happening in crypto, including social sentiment and important headlines.")))
    metta.space().add_atom(E(S("news"), S("professional"), S("specific"), ValueAtom("Provide a professional, detailed summary of news or sentiment regarding this specific coin or event.")))
    metta.space().add_atom(E(S("news"), S("casual"), S("specific"), ValueAtom("Explain the latest news or social sentiment for this coin in an easy, casual way.")))

    if not os.path.exists("knowledge.metta"):
        with open("knowledge.metta", "w") as _: pass
    else:
        with open("knowledge.metta", "w") as file:
            for line in file.readlines():
                metta.run(line.strip())

def add_to_knowlegde_graph(atom: str):
    
    # Simple cache.
    metta.run(atom.strip())
    with open("knowledge.metta", "a") as file:
        file.write(atom.strip())