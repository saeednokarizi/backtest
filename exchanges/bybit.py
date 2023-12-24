from typing import *
import logging


import requests


logger = logging.getLogger()

class BybitClient:
    def __init__(self):
        self._base_url = "https://api.bybit.com"
        self.symbols = self._get_symbols()
        if self.symbols is None:
            self.symbols = []

    def _make_requests(self, endpoint: str, query_parameters: dict=None):
        if query_parameters is None:
            query_parameters = {}
        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
            response.raise_for_status()
        except Exception as e:
            print(f"Exception when making request to {endpoint}: {e}")  # Add this line
            logger.error("Connection Error while making request to %s: %s", endpoint, e)
            return None

        try:
            return response.json()
        except ValueError:
            logger.error("Error decoding JSON response from %s: %s", endpoint, response.text)
            return None
'''
    def _get_symbols(self) -> List[str]:
        endpoint = "/v2/public/symbols"
        data = self._make_requests(endpoint)

        print(f"Data from {endpoint}: {data}")  # Add this line
        #print("Full data response:", data)  # Print the full data response

        if data is not None and 'result' in data:
            symbols = [x["name"] for x in data["result"]["list"] if "name" in x]

        else:
            #print("No data received from the endpoint.")
            return []
'''
def _get_symbols(self) -> List[str]:
        endpoint = "/v2/public/symbols"
        data = self._make_requests(endpoint)

        if data is not None and 'result' in data:
            symbols = [x["name"] for x in data["result"] if "name" in x]
        else:
            return []

        return symbols
            
    def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None, category: str = 'inverse'):
        params = dict()
        params["symbol"] = symbol
        params["interval"] = 60
        params["limit"] = 1000
        params["category"] = category

        if start_time is not None:
            params["start"] = start_time
        if end_time is not None:
            params["end"] = end_time

        print(f"Fetching data for {symbol} from {start_time} to {end_time}")

        endpoint = "/v5/market/kline"
        raw_candles = self._make_requests(endpoint, params)
        print("Raw candles:", raw_candles)  

        candles = []

        if raw_candles is not None:
            for c in raw_candles['result']['list']:
                candles.append((float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5]), float(c[6])))
            return candles
        else:
            print(f"No data received for {symbol} from {start_time} to {end_time}")
            return None
