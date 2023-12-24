from typing import *
import logging

import requests

from datetime import datetime



logger = logging.getLogger()


class BybitClient:
    def __init__(self):
        self._base_url = "https://api.bybit.com"

        self.symbols = self._get_symbols()

    def _make_requests(self, endpoint: str, query_parameters: Dict):

        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
            print(response.status_code)  # Print the status code
            print(response.json())  # Print the response data
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)
            return None

        if response.status_code == 200:
            json_response = response.json()
            print(json_response)  # Add this line
            if "ret_msg" in json_response and json_response["ret_msg"] == "OK":
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
        endpoint = "/v2/public/symbols"
        data = self._make_requests(endpoint, None)

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
            params["start_time"] = int(start_time / 1000)
        if end_time is not None:
            params["end_time"] = int(end_time / 1000)

        endpoint = "/v5/market/kline"
        raw_candles = self._make_request(endpoint, params)
        

        candles = []

        if raw_candles is not None:
            for c in raw_candles['list']:
                ts = datetime.fromtimestamp(int(c[0]) / 1000)
                ts_millis = int(round(ts.timestamp() * 1000))
                candles.append((ts_millis, float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5]),))
            
            return candles
        else:
            return None
            
