from utils.urls import construct_request_url
from core.fetch_data import get_data
import json
from algo.run_pipeline import run_algo
import matplotlib.pyplot as plt

nifty_50 = ["HDFCBANK.BSE", "TATASTEEL.BSE", "INFY.BSE"]

for stock in nifty_50:
    url = construct_request_url("TIME_SERIES_DAILY", "5min", stock)
    data = get_data(url)

    #Save into a JSON file
    with open(f"data/{stock}_data.json", "w") as file:
        json.dump(data, file, indent=4)


file_path = "data/TATASTEEL.BSE_data.json"

run_algo(file_path)
