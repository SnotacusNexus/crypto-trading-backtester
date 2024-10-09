from data_fetcher import DataFetcher
from strategy import TradingStrategy
from backtester import Backtester
from datetime import datetime, timedelta

def main():
    # Initialize DataFetcher and get available symbols
    fetcher = DataFetcher()
    symbols = fetcher.get_available_symbols()

    if not symbols:
        print("No symbols available. Exiting.")
        return

    # Choose the first symbol for demonstration
    symbol = symbols[0]
    print(f"Running backtest for {symbol}")

    # Fetch historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # 1 year of data
    data = fetcher.fetch_data(symbol, '1d', int(start_date.timestamp() * 1000), 365)

    if data is None:
        print("Failed to fetch data. Exiting.")
        return

    # Initialize strategy and backtester
    strategy = TradingStrategy(short_window=50, long_window=200)
    backtester = Backtester(strategy, data)

    # Run backtest
    backtester.run()

    # Plot results
    backtester.plot_results()

    # Print performance metrics
    metrics = backtester.get_performance_metrics()
    print("Performance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
