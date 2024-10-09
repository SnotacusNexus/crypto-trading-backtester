import pandas as pd

class MovingAverageCrossoverStrategy:
    def __init__(self, short_window: int, long_window: int):
        self.name = f"MA Crossover ({short_window}, {long_window})"
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = pd.Series(index=data.index, dtype=int)
        signals.iloc[:] = 0

        # Calculate moving averages
        short_ma = data['close'].rolling(window=self.short_window).mean()
        long_ma = data['close'].rolling(window=self.long_window).mean()

        # Generate buy and sell signals
        signals[short_ma > long_ma] = 1  # Buy signal
        signals[short_ma < long_ma] = -1  # Sell signal

        return signals
