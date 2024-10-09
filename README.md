# Cryptocurrency Trading Strategy Backtester

This project implements a simple cryptocurrency trading strategy backtester using the CCXT library to fetch data from the MEXC exchange.

## Features

- Fetches historical price data from MEXC exchange
- Implements a Moving Average Crossover strategy
- Calculates key performance metrics: Total Return, Sharpe Ratio, and Maximum Drawdown
- Provides a framework for testing different trading strategies

## Usage

1. Install the required dependencies:
   ```
   pip install ccxt pandas numpy matplotlib
   ```

2. Run the main script:
   ```
   python src/main.py
   ```

3. The script will output the backtest results for the Moving Average Crossover strategy.

## Customization

- To implement your own strategy, create a new class in `src/strategy.py` following the structure of the `MovingAverageCrossoverStrategy` class.
- Modify the `main.py` script to use your custom strategy.
- Adjust the symbol, timeframe, and date range in `main.py` to backtest different scenarios.

## Future Improvements

- Implement more sophisticated trading strategies
- Add support for multiple exchanges
- Improve visualization of backtest results
- Implement portfolio management and risk assessment features

