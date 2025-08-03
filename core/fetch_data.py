import requests


def get_data(url: str):
    """
    Fetches data from the given URL.
    Args:
        url (str): The URL to fetch data from.
    Returns:
        dict: The JSON response from the API.
    """
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}