import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

def construct_request_url(function: str, interval: str, symbol: str):
    """
    Constructs the API request URL for Alpha Vantage.
    Args:
        function (str): The function to be used in the API request.
        interval (str): The interval for the data.
        symbol (str): The stock symbol for which data is requested.
    Returns:
        str: The constructed API request URL.
    """
    base_url = "https://www.alphavantage.co/query"

    return f"{base_url}?function={function}&symbol={symbol}&outputsize=full&apikey={os.getenv('ALPHA_VANTAGE_KEY')}"
