from typing import *
import logging


import requests


logger = logging.getLogger()

class BinanceClient:
    def __init__(self, futures=False):
        self.futures = futures
        if self.futures:
            self._base_url = "https://fapi.binance.com"

        else:
            self._base_url = "https://api.binance.com"

        self.symbols = self._get_symbols()

    def _make_requests(self, endpoint: str, query_parameters: dict):
    
        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
        except Exception as e:
            logger.error("Connection Error while making request to %s: %s", endpoint, e)
            return None
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making request to %s: %s (status code = %s)",
                          endpoint, response.json(), response.status_code)
            return None
    
    def _get_symbols(self):
        params = dict()
       # endpoint = "/fapi/v1/exchangeInfo" if self.futures else "/api/v3/exchangeInfo"
        endpoint = "/api/v3/exchangeInfo"
        data = self._make_requests(endpoint, params)
        print(data)