from typing import List, Any
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

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
        if tools == None or len(tools) == 0:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools or []
            )

    
    return response

def asi_request_with_retry(messages, tools, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return asi_request(messages, tools=tools, max_tokens=6000)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(delay)

    raise RuntimeError("Max retries reached")

def get_structured_output(response):
    if not response.choices[0].message.tool_calls:
        raise RuntimeError("No structured output.")
    return json.loads(response.choices[0].message.tool_calls[0].function.arguments)