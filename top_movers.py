import requests  # Requêtes HTTP

def get_top_movers():  # Fonction pour récupérer 10 top gainers
    url = "https://api.coingecko.com/api/v3/coins/markets"  # Endpoint API
    params = {  # Paramètres de requête
        "vs_currency": "usd",  # Devise dollar
        "order": "percent_change_24h_desc",  # Tri par gain
        "per_page": 10,  # Obtenir 10 pièces
        "page": 1,  # Première page
        "sparkline": False  # Sans données sparkline
    }
    response = requests.get(url, params=params)  # Appel API
    if response.status_code == 200:  # Si réussite
        return response.json()  # Retourner données
    else:
        return []  # Retourner liste vide
