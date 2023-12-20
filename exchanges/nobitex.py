from typing import *
import logging


import requests


logger = logging.getLogger()
class NobitexClient:
    def __init__(self):
        self._base_url = "https://api.nobitex.ir"
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
        endpoint = "/v2/orderbook/all"
        data = self._make_requests(endpoint, params)
        print(data)