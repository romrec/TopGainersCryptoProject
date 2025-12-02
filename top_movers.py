import requests  # HTTP requests

def get_top_movers():  # Function to get 10 top gainers
    url = "https://api.coingecko.com/api/v3/coins/markets"  # Api endpoint
    params = {  # Query params
        "vs_currency": "usd",  # Dollar iso
        "order": "percent_change_24h_desc",  # Sort by gain
        "per_page": 10,  # Get 10 coins
        "page": 1,  # First page
        "sparkline": False  # No sparkline data
    }
    response = requests.get(url, params=params)  # Make API call
    if response.status_code == 200:  # If successful
        return response.json()  # Return data
    else:
        return []  # Return empty list
