import requests


class BybitClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def get_kline_data(self, symbol, interval, limit):
        base_url = "https://api.bybit.com/v5/market/kline"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        
        # convert data to Pydantic schema?

        return data
