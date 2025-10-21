from collections.abc import Callable
import inspect
from typing import get_args, get_type_hints, Annotated
import os
import requests
from dotenv import load_dotenv
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel, Field
from openai import pydantic_function_tool
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types


load_dotenv()

class Sentiment(BaseModel):
    sentiment: float = Field(..., description='Number between -1 and 1. -1 Means extremely negative sentiment. 1 means extremely positive sentiment. 0 is netural.')

sentiment_tool = pydantic_function_tool(
    Sentiment,
    name="sentiment",
    description="Detect whether an image has a positive or negative sentiment."
)

def create_tool_schema(func: Callable):
    """ Creates schema for simple functions without json/pydict parameters. """

    params = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
    mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
    }

    sig = inspect.signature(func)
    hints = get_type_hints(func, include_extras=True)
    for name, param in sig.parameters.items():
        base_type, description = get_args(hints[name])
        params["properties"][name] = {"type": mapping[base_type], "description": description}
        if param.default is inspect.Parameter.empty:
            params["required"].append(name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": params,
            "strict": True
        }
    }
    
def fear_and_greed_index(limit: Annotated[int, "Days in past of greed/fear to get."]):
    """ Gets fear and greed index for a specified timespan. """

    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    api_key = os.getenv("COINMARKETCAP_KEY")
    
    headers = {
        "X-CMC_PRO_API_KEY": api_key
    }
    
    params = {
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)

    return [x for x in response.json()["data"]]

def social_sentiment(time_period: Annotated[str, "Time period to get posts from. Must be \"day\", \"week\", or \"month\""], coin: Annotated[str, "Coin to check sentiment on. Blank for checking whole market sentiment."] = ""):
    
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_KEY"),
        client_secret=os.getenv("REDDIT_KEY"),
        user_agent="calculating social sentiment"
    )

    subreddit = reddit.subreddit("CryptoCurrency") 
    if coin != "":  
        search_results = list(reddit.subreddits.search(coin, limit=1))
        if search_results:
            search_sub = search_results[0]
            if search_sub.subscribers and search_sub.subscribers > 10000:
                subreddit = search_sub

    posts = []
    for post in subreddit.top(limit=20, time_filter=time_period):
        if post.is_self and len(post.selftext) > 50:
            posts.append({
                "title": post.title,
                "body": post.selftext
            })
        elif post.url.endswith((".jpg", ".png", ".jpeg")):
            posts.append({
                "title": post.title,
                "url": post.url
            })

    class Sentiment(BaseModel):
        sentiment: Annotated[float, "Number from -1 to 1."]

    # VADER analyzer for text and google genai for images.
    analyzer = SentimentIntensityAnalyzer()
    client = genai.Client(api_key=os.getenv("GOOGLE_KEY"))
    
    #score = analyzer.polarity_scores(text)
    # image_path = "https://i.redd.it/tt4aevxlg2wf1.jpeg"
    # image_bytes = requests.get(image_path).content
    # image = types.Part.from_bytes(
    # data=image_bytes, mime_type="image/jpeg"
    # )

    # client = genai.Client(api_key=os.getenv("GOOGLE_KEY"))
    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=["Give a number from -1 to 1 where -1 is extremely negative sentiment, 0 is netural, and 1 is extremely positive sentiment.", image],
    #     config={
    #         "response_mime_type": "application/json",
    #         "response_schema": Sentiment
    #     }
    # )
    #response.text["sentiment"]

