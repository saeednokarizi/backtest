import requests

def get_ticker(symbol: str):
    response = requests.get(f"https://api.bybit.com/v2/public/tickers?symbol={symbol}")
    data = response.json()

    if data['ret_code'] == 0:
        return data['result']
    else:
        return None

ticker_data = get_ticker("BTCUSDT")
print(ticker_data)
