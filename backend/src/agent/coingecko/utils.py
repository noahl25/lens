import requests
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

def coingecko_request(endpoint: str):
    url = f"https://api.coingecko.com/api/v3{endpoint}"
    headers = {"x-cg-demo-api-key": os.getenv("COINGECKO_KEY")}
    return requests.get(url, headers=headers).json()

@lru_cache(maxsize=128)
def get_id(query: str):
    result = coingecko_request(f"/search?query={query}")
    if len(result) > 0:
        return result["coins"][0]["id"]
    else:
        raise RuntimeError("Query returns no results.")