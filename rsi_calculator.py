from pandas import DataFrame
from ta import momentum
from decimal import Decimal

def calculate_rsi(closing_prices: list):
    df = DataFrame({"close": closing_prices})
    df["rsi"] = momentum.RSIIndicator(df["close"]).rsi()
    return df["rsi"].values[-1]

def get_closing_prices(data: dict) -> list[Decimal]:
    closing_prices = [Decimal(candle[4]) for candle in data['result']['list']]
    return closing_prices
