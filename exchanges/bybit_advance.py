from typing import *
import logging

import requests
import dateutil.parser
from datetime import datetime



logger = logging.getLogger()


class BybitClient:
    def __init__(self):
        self._base_url = "https://api.bybit.com"

        self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):

        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)
            return None

        if response.status_code == 200:
            json_response = response.json()
            if "retMsg" in json_response and json_response["retMsg"] == "OK":
                return json_response["result"]
            else:
                logger.error("Error while making request to %s: %s (status code = %s)",
                             endpoint, json_response, response.status_code)
                return None
        else:
            logger.error("Error while making request to %s: %s (status code = %s)",
                         endpoint, response.json(), response.status_code)
            return None

    def _get_symbols(self) -> List[str]:

        params = dict()

        endpoint = "/v2/public/symbols"
        data = self._make_request(endpoint,{})
        #symbols = [x["name"] for x in data["result"] if "name" in x]
        if data is not None:
            symbols = [x["name"] for x in data]
            return symbols

    def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None, category: str = 'inverse'):
        
        params = dict()
        params["symbol"] = symbol
        params["interval"] = 60
        params["limit"] = 1000
        params["category"] = category

        if start_time is not None:
            params["start_time"] = int(start_time / 1000)
        if end_time is not None:
            params["end_time"] = int(end_time / 1000)

        endpoint = "/v5/market/kline"
        raw_candles = self._make_request(endpoint, params)
        

        candles = []

        if raw_candles is not None:
            for c in raw_candles['list']:
                ts = datetime.fromtimestamp(int(c[0]) / 1000)
                candles.append((ts, float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5]),))
            
            return candles
        else:
            return None







