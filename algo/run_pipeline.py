import json
import pandas as pd
from core.indicators import load_data, compute_indicators
from core.strategy import backtest_strategy
from core.ml_model import train_predict
from core.sheets_logger import setup_gsheet, log_trades

def run_algo(file_path):
    with open(file_path) as f:
        av_json = json.load(f)

    df = load_data(av_json)
    df = compute_indicators(df)
    df = backtest_strategy(df)
    # df, acc, model = train_predict(df)

    # print(f"✅ ML Accuracy: {acc:.2%}")
    logs, pnl, summary = setup_gsheet()
    log_trades(df, logs)

