import ccxt
from strategy import MovingAverageCrossoverStrategy
from backtester import Backtester

def main():
    exchange = ccxt.mexc()
    symbol = 'BTC/USDT'
    timeframe = '1h'
    
    backtester = Backtester(exchange, symbol, timeframe)
    strategy = MovingAverageCrossoverStrategy(short_window=50, long_window=200)
    
    results = backtester.run_backtest(strategy, '2023-01-01T00:00:00Z', '2023-12-31T23:59:59Z')
    print(f"Backtest Results for {strategy.name}:")
    print(f"Total Return: {results['total_return']:.2%}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2%}")

    # Uncomment the following line to display the plot (Note: This won't work in a headless environment)
    # backtester.plot_results(data, signals)

if __name__ == "__main__":
    main()
