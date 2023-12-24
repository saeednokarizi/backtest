import logging

from exchanges.bybit import BybitClient
from exchanges.binance import BinanceClient
#from exchanges.bybit_advance import BybitClient

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

#logger.info("this is a info log")

if __name__ == "__main__":
    
    mode = input("Choose the program mode (data / backtest / optimize): ").lower()
    while True:
        exchange = input("choose an exchange: ").lower()
        if exchange in ("binance", "bybit"):
            break

    if exchange == "binance":
        client = BinanceClient()
        
    elif exchange == "bybit":
        client = BybitClient()

    if not client.symbols:
        print("Error: No symbols found.")
        exit(1)
    #print(client.symbols)  # Add this line
        
    #print(client.get_historical_data("BTCUSDT"))   

    while True:
        symbol = input("choose a symbol: ").upper()
        if symbol in client.symbols :
            break
