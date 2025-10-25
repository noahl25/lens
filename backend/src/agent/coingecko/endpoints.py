from typing import Annotated
from .utils import coingecko_request, get_id
import datetime

def coin_general_data(coin_id: Annotated[str, "Fully qualified name of coin. E.g. 'bitcoin' or 'ethereum'. If unknown, pass coin name directly from user query."]):
    """
    Get the current market snapshot for a coin — includes live price,
    24h performance, market cap, supply, and other real-time metrics.
    This is best for general data. Use alongside historical_data for best metrics.
    """
    return coingecko_request(f"/coins/markets?vs_currency=usd&ids={get_id(coin_id)}")

def historical_data(coin_id: Annotated[str, "Fully qualified name of coin. E.g. 'bitcoin' or 'ethereum'. If unknown, pass coin name directly from user query."], days: Annotated[int, "Days in past to get data from."], metric: Annotated[str, "Metric to get. Must be 'prices', 'market_caps', or 'total_volumes'. Leave blank for all metrics."] = ""):
    """
    Get historical time-series data for a coin — including prices, volume,
    and market cap across a time range. Data is suitable for charts and
    trend analysis.

    Use this when the user mentions:
      - historical prices (day/week/month/year)
      - chart data
      - trend or volatility insights
      - 'how has price moved over time?'
    
    This is best for data.
    """
    response = coingecko_request(f"/coins/{get_id(coin_id)}/market_chart?days={days}&vs_currency=usd")
    for key in ["prices", "market_caps", "total_volumes"]:
        for point in response[key]:
            point[0] = datetime.datetime.fromtimestamp(
                point[0] / 1000, 
                tz=datetime.timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")
            point[1] = str(point[1])

    if metric != "":
        response = {metric: response[metric]}

    return response

