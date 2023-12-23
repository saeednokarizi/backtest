from typing import *
import logging


import requests


logger = logging.getLogger()

class BybitClient:
    def __init__(self):
        self._base_url = "https://api.bybit.com"
        self.symbols = self._get_symbols()

    def _make_requests(self, endpoint: str, query_parameters: dict=None):
        if query_parameters is None:
            query_parameters = {}
        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
            response.raise_for_status()
        except Exception as e:
            logger.error("Connection Error while making request to %s: %s", endpoint, e)
            return None

        try:
            return response.json()
        except ValueError:
            logger.error("Error decoding JSON response from %s: %s", endpoint, response.text)
            return None

    def _get_symbols(self) -> List[str]:
        endpoint = "/v2/public/symbols"
        data = self._make_requests(endpoint)
    
        print("Full data response:", data)  # Print the full data response

        if data is not None and 'result' in data:
            symbols = [item["name"] for item in data["result"]]
            print("Symbols:", symbols)  # Print the extracted symbols
            return symbols
        else:
            print("No data received from the endpoint.")
            return []
            
    def get_historical_data(self, symbole: str, start_time: Optional[int] = None, end_time: Optional[int] = None ):

        params = dict()

        params["symbol"] = symbol
        params["interval"] = "1m"
        params["limit"] = 1000

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time

        endpoint = "/v5/market/kline"
        raw_candles = self._make_requests(endpoint, params)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append((float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])))
            return candles
        else:
            return None