import pandas as pd
import numpy as np

def load_data(av_json):
    """Converts Alpha Vantage JSON (Time Series) to DataFrame."""
    ts_key = next(k for k in av_json if "Time Series (Daily)" in k)
    data = av_json[ts_key]
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def calculate_dma(df, short=20, long=50):
    df["DMA20"] = df["close"].rolling(window=short).mean()
    df["DMA50"] = df["close"].rolling(window=long).mean()
    df["DMA_Cross"] = (df["DMA20"] > df["DMA50"]).astype(int).diff().fillna(0).clip(lower=0)
    return df

def compute_rsi(df, window=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_macd(df, short_window=12, long_window=26, signal_window=9):
    ema_short = df['close'].ewm(span=short_window, adjust=False).mean()
    ema_long = df['close'].ewm(span=long_window, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def compute_indicators(df):
    df = df.copy()
    df['RSI'] = compute_rsi(df)
    df['20DMA'] = df['close'].rolling(window=20).mean()
    df['50DMA'] = df['close'].rolling(window=50).mean()
    df['MACD'], df['MACD_signal'] = compute_macd(df)

    # Ensure Volume exists; if not, fill with dummy (you can adjust this based on your real data)
    if 'volume' in df.columns:
        df['Volume'] = df['volume']
    else:
        df['Volume'] = 0  # or df['close'].rolling(3).std() etc.

    return df