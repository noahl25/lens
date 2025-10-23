from typing import Annotated
from utils import coingecko_request

def coin_market_data(coin_id: Annotated[str, "Fully qualified name of coin. E.g. 'bitcoin' or 'ethereum'."]):
    """ Gets various data about coin. E.g. High 24hr, Low 24hr, Price Change 24hr."""
    return coingecko_request(f"/coins/markets?vs_currency=usd&ids={coin_id}")

def historical_data(coin_id: Annotated[str, "Fully qualified name of coin. E.g. 'bitcoin' or 'ethereum'."], days: Annotated[int, "Days in past to get data from."]):
    """ Gets price, volume, and market cap for specified number of days. """
    return coingecko_request(f"/coins/{coin_id}/market_chart?days={days}&vs_currency=usd")

print(coin_market_data("bitcoin"))