import ccxt
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self):
        self.exchange = ccxt.mexc({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

    def fetch_data(self, symbol, timeframe, since, limit):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def get_available_symbols(self):
        try:
            markets = self.exchange.load_markets()
            return [symbol for symbol, market in markets.items() if market['future']]
        except Exception as e:
            print(f"Error fetching available symbols: {e}")
            return []
