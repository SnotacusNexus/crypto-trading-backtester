import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
from datetime import datetime

class Backtester:
    def __init__(self, exchange: ccxt.Exchange, symbol: str, timeframe: str):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch_data(self, since: str, limit: int) -> pd.DataFrame:
        since_ts = int(datetime.fromisoformat(since.replace('Z', '+00:00')).timestamp() * 1000)
        
        ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, since=since_ts, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    def run_backtest(self, strategy, start_date: str, end_date: str) -> Dict:
        data = self.fetch_data(start_date, 1000)
        signals = strategy.generate_signals(data)
        
        # Calculate returns
        data['returns'] = data['close'].pct_change()
        data['strategy_returns'] = data['returns'] * signals.shift(1)
        
        # Calculate performance metrics
        total_return = (1 + data['strategy_returns']).prod() - 1
        sharpe_ratio = np.sqrt(252) * data['strategy_returns'].mean() / data['strategy_returns'].std()
        max_drawdown = (data['close'] / data['close'].cummax() - 1).min()
        
        return {
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown
        }

    def plot_results(self, data: pd.DataFrame, signals: pd.Series):
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['close'], label='Close Price')
        plt.plot(data.index, data['close'].rolling(window=50).mean(), label='50-day MA')
        plt.plot(data.index, data['close'].rolling(window=200).mean(), label='200-day MA')
        
        plt.plot(data.index[signals == 1], data['close'][signals == 1], '^', markersize=10, color='g', label='Buy Signal')
        plt.plot(data.index[signals == -1], data['close'][signals == -1], 'v', markersize=10, color='r', label='Sell Signal')
        
        plt.title(f"{self.symbol} Price Chart with Signals")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()
