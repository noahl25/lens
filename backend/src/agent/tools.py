from collections.abc import Callable
import inspect
from typing import get_args, get_type_hints, Annotated, cast, Literal, Dict
import os
import requests
from dotenv import load_dotenv
import asyncpraw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pydantic import BaseModel, Field
from openai import pydantic_function_tool
from google import genai
from google.genai import types
from datetime import datetime
import json
from tavily import TavilyClient
import aiohttp
import asyncio
from collections import defaultdict

from prompts import IMAGE_SENTIMENT_PROMPT

load_dotenv()

def create_tool_schema(func: Callable):
    """ Creates schema for simple functions without json parameters. """

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
    """ Gets fear and greed index for a specified timespan. Gives a number from 0 to 100, where 0 is extreme fear and 100 is extreme greed. """

    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    
    headers = {
        "X-CMC_PRO_API_KEY": os.getenv("COINMARKETCAP_KEY")
    }
    
    params = {
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)

    return [x for x in response.json()["data"]]

async def analyze_image_sentiment(session, client, post, index = 0) -> Dict:

    image_url = post["url"]

    async with session.get(image_url) as resp:
        image_bytes = await resp.read()

    image = types.Part.from_bytes(
        data=image_bytes,
        mime_type=f"image/{image_url.split('.')[-1]}"
    )
    class Sentiment(BaseModel):
        sentiment: Annotated[float, "Number from -1 to 1."]
        short_description: Annotated[str, "Short description of image."]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[IMAGE_SENTIMENT_PROMPT + post["title"], image],
        config={
            "response_mime_type": "application/json",
            "response_schema": Sentiment
        }
    )

    result = json.loads(response.text)

    return {
        "sentiment_score": result["sentiment"],
        "image_description": result["short_description"],
        "date": post["date"],
        "datestr": post["datestr"],
        "post_link": post.shortlink,
        "index": index
    }

async def get_top_reddit(time_period: str, coin: str = "", image_descriptions: bool = False):

    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_KEY"),
        client_secret=os.getenv("REDDIT_KEY"),
        user_agent="calculating social sentiment"
    )

    subreddit = await reddit.subreddit("CryptoCurrency") 
    if coin != "":
        search_sub = None
        async for sr in reddit.subreddits.search(coin, limit=1):
            search_sub = sr
            break
        if search_sub:
            if search_sub.subscribers > 10000:
                subreddit = search_sub

    limit = 5
    env_limit = os.getenv("REDDIT_API_LIMIT")
    if env_limit and env_limit != "":
        limit = int(env_limit)

    posts = []
    async for post in subreddit.top(limit=limit, time_filter=time_period):
        if post.is_self:
            posts.append({
                "title": post.title,
                "body": post.selftext,
                "date": float(post.created_utc),
                "datestr": datetime.fromtimestamp(post.created_utc).strftime("%m/%d/%Y"),
                "type": "text",
                "post_link": post.shortlink
            })
        elif post.url.endswith((".jpg", ".png", ".jpeg")):
            posts.append({
                "title": post.title,
                "url": post.url,
                "date": float(post.created_utc),
                "datestr": datetime.fromtimestamp(post.created_utc).strftime("%m/%d/%Y"),
                "type": "image",
                "post_link": post.shortlink
            })
        else:
            posts.append({
                "title": post.title,
                "body": "",
                "date": float(post.created_utc),
                "datestr": datetime.fromtimestamp(post.created_utc).strftime("%m/%d/%Y"),
                "type": "title",
                "post_link": post.shortlink
            })

    if image_descriptions:
        image_tasks = []
        client = genai.Client(api_key=os.getenv("GOOGLE_KEY"))
        async with aiohttp.ClientSession() as session:
            for id, post in enumerate(posts):
                if post["type"] == "image":
                    image_tasks.append(
                        analyze_image_sentiment(session, client, post, id)
                    )
            image_results = await asyncio.gather(*image_tasks)
            for result in image_results:
                posts[result["index"]]["image_description"] = result["image_description"]

    await reddit.close()
    return posts

async def social_sentiment(time_period: str, coin: str = ""):
    
    posts = await get_top_reddit(time_period, coin)

    # VADER analyzer for text and google genai for images.
    analyzer = SentimentIntensityAnalyzer()
    client = genai.Client(api_key=os.getenv("GOOGLE_KEY"))

    results = []
    image_tasks = []
    async with aiohttp.ClientSession() as session:
        try:
            for post in posts:
                if post["type"] == "text" or post["type"] == "title":
                    score = analyzer.polarity_scores(f"{post['title']} {post['body']}")
                    results.append({
                        "sentiment_score": score["compound"],
                        "date": post["date"],
                        "datestr": post["datestr"],
                        "body": post["body"],
                        "post_link": post["post_link"]
                    })
                elif post["type"] == "image":
                    image_tasks.append(
                        analyze_image_sentiment(session, client, post)
                    )
            image_results = await asyncio.gather(*image_tasks)
        except Exception as e:
            print(e)

    results.extend(image_results)
    results = sorted(results, key=lambda item: item["date"])

    daily_scores = defaultdict(list)
    for item in results:
        if "sentiment_score" in item:
            daily_scores[item["datestr"]].append(item["sentiment_score"])

    daily_averages = [
        {"datestr": date, "average_sentiment": sum(scores)/len(scores)}
        for date, scores in daily_scores.items()
    ]

    overall_avg = sum([item["sentiment_score"] for item in results if "sentiment_score" in item]) / len([item for item in results if "sentiment_score" in item])

    results.append({
        "average_sentiments": {
            "overall_average_sentiment": overall_avg,
            "daily_averages": daily_averages
        }
    })

    return results

def social_sentiment_tool(time_period: Annotated[str, "Time period to get posts from. Must be \"day\", \"week\", or \"month\""], coin: Annotated[str, "Coin to check sentiment on. Blank for checking whole market sentiment."] = ""):
    """ Gets social sentiment of a coin in a specified range. """
    return asyncio.run(social_sentiment(time_period, coin))

def get_top_reddit_tool(time_period: Annotated[str, "Time period to get posts from. Must be \"day\", \"week\", or \"month\""], coin: Annotated[str, "Coin to get posts from."] = ""):
    """ Gets top posts from reddit for a coin in a specified range. Good for getting news and the latest. Best for when wanting more personal and casual news."""
    return asyncio.run(get_top_reddit(time_period, coin, image_descriptions=True))

def web_search(time_period: Annotated[str, "Time period to search. Must be \"day\", \"week\", \"month\", or \"year\""], query: Annotated[str, "Query to search. Should only be 1-3 keywords."]):
    """ Searches for relevant articles and data based on the query. Good for news and recent information. Call alongside get_top_reddit_tool for most well-rounded news, if needed. """
    if time_period not in ["day", "week", "month", "year"]:
        raise ValueError("time_period must be one of: day, week, month, year")

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_KEY"))
    response = tavily_client.search(query, topic="news", time_range=cast(Literal['day', 'week', 'month', 'year'], time_period), max_results=10)
    for result in response["results"]:
        result["post_link"] = result.pop("url")
    return response["results"]

import coingecko.endpoints
coingecko_functions = inspect.getmembers(coingecko.endpoints, inspect.isfunction)

TOOLS_REF = [
    social_sentiment_tool,
    get_top_reddit_tool,
    web_search,
    fear_and_greed_index,
    *[func for _, func in coingecko_functions if func.__module__ == coingecko.endpoints.__name__]
]

TOOLS_FORMATTED = [
    create_tool_schema(func) for func in TOOLS_REF
]

TOOLS_DICT = {func.__name__: func for func in TOOLS_REF}

print(TOOLS_FORMATTED)