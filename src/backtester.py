import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Backtester:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data
        self.initial_capital = 100000.0
        self.positions = None
        self.portfolio = None

    def run(self):
        signals = self.strategy.generate_signals(self.data)
        self.positions = self.generate_positions(signals)
        self.portfolio = self.backtest_portfolio()

    def generate_positions(self, signals):
        positions = pd.DataFrame(index=signals.index).fillna(0.0)
        positions['BTC'] = 100 * signals['signal']
        return positions

    def backtest_portfolio(self):
        portfolio = self.positions.multiply(self.data['close'], axis=0)
        pos_diff = self.positions.diff()

        portfolio['holdings'] = (self.positions.multiply(self.data['close'], axis=0)).sum(axis=1)
        portfolio['cash'] = self.initial_capital - (pos_diff.multiply(self.data['close'], axis=0)).sum(axis=1).cumsum()

        portfolio['total'] = portfolio['cash'] + portfolio['holdings']
        portfolio['returns'] = portfolio['total'].pct_change()
        return portfolio

    def plot_results(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))
        
        self.data['close'].plot(ax=ax1)
        ax1.plot(self.data.index, self.strategy.generate_signals(self.data)['short_mavg'], label='Short MA')
        ax1.plot(self.data.index, self.strategy.generate_signals(self.data)['long_mavg'], label='Long MA')
        ax1.set_ylabel('Price')
        ax1.set_title('Price and Moving Averages')
        ax1.legend()

        self.portfolio['total'].plot(ax=ax2)
        ax2.set_ylabel('Portfolio value')
        ax2.set_title('Portfolio Performance')

        plt.tight_layout()
        plt.savefig('backtesting_results.png')
        plt.close()

    def get_performance_metrics(self):
        total_return = (self.portfolio['total'][-1] - self.initial_capital) / self.initial_capital
        sharpe_ratio = np.sqrt(252) * self.portfolio['returns'].mean() / self.portfolio['returns'].std()
        max_drawdown = (self.portfolio['total'] / self.portfolio['total'].cummax() - 1).min()

        return {
            'Total Return': f'{total_return:.2%}',
            'Sharpe Ratio': f'{sharpe_ratio:.2f}',
            'Max Drawdown': f'{max_drawdown:.2%}'
        }
