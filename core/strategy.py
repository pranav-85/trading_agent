import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def prepare_df(df):
    """
    Cleans and filters the input DataFrame:
    - Ensures datetime index
    - Converts 'close' column to float
    - Filters for last 6 months
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    if "close" not in df.columns:
        raise ValueError("❌ DataFrame must contain a 'close' column.")

    df["close"] = df["close"].astype(float)

    six_months_ago = datetime.now() - timedelta(days=180)
    df = df[df.index >= six_months_ago]

    return df


def compute_rsi(df, window=14):
    """
    Calculates the RSI indicator.
    """
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    
    rs = avg_gain / (avg_loss + 1e-10)
    df["RSI"] = 100 - (100 / (1 + rs))
    
    return df


def compute_moving_averages(df):
    """
    Adds 20DMA and 50DMA columns.
    """
    df["20DMA"] = df["close"].rolling(window=20).mean()
    df["50DMA"] = df["close"].rolling(window=50).mean()
    return df


def detect_signals(df):
    """
    Flags:
    - RSI < 30 as oversold
    - 20DMA crossing above 50DMA as bullish crossover
    - Final_Buy_Signal = both conditions true
    """
    df["RSI_Buy"] = df["RSI"] < 30

    dma_crossover = (
        (df["20DMA"] > df["50DMA"]) & 
        (df["20DMA"].shift(1) <= df["50DMA"].shift(1))
    )
    df["DMA_Crossover"] = dma_crossover

    df["Final_Buy_Signal"] = df["RSI_Buy"] & df["DMA_Crossover"]
    return df


def backtest_strategy(df):
    """
    Runs the backtest pipeline: clean df, add indicators,
    detect signals, print buy signals, plot results.
    """
    df = prepare_df(df)
    df = compute_rsi(df)
    df = compute_moving_averages(df)
    df = detect_signals(df)

    buy_signals = df[df["Final_Buy_Signal"]]
    print(f"✅ Total Buy Signals in last 6 months: {len(buy_signals)}")
    print(buy_signals[["close", "RSI", "20DMA", "50DMA"]])

    # plot results
    plt.figure(figsize=(14, 6))
    plt.plot(df.index, df["close"], label="Close Price", alpha=0.5)
    plt.plot(df.index, df["20DMA"], label="20 DMA", linestyle="--", color="blue")
    plt.plot(df.index, df["50DMA"], label="50 DMA", linestyle="--", color="red")
    plt.scatter(buy_signals.index, buy_signals["close"], 
                label="Buy Signal", marker="^", color="green")
    plt.title("Buy Signals (RSI < 30 & 20DMA > 50DMA)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return buy_signals
