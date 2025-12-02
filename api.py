import requests

def get_top_movers():
    """
    Récupère les top gainer de crypto-monnaies via CoinGecko API.

    Returns:
        list: Liste des 10 crypto-monnaies triées par changement de prix en 24h (desc.).
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "percent_change_24h_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []
