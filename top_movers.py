import requests
import logging

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"  # Endpoint API CoinGecko


def get_top_movers(limit=10):
    """Récupère les N crypto-monnaies avec la meilleure variation sur 24h.

    Comme l'endpoint dédié aux top gainers est réservé à l'API payante CoinGecko,
    on récupère les 250 premières cryptos par market cap et on trie côté Python
    par variation 24h décroissante.

    Args:
        limit : Nombre de résultats à retourner (défaut: 10)

    Returns:
        Liste de dicts avec les données CoinGecko triés par variation 24h,
        ou liste vide en cas d'erreur réseau ou réponse invalide.
    """
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",          # Seul tri valide sur l'API gratuite
        "per_page": 250,                     # Maximum autorisé en compte gratuit
        "page": 1,
        "sparkline": False,                  # Sans données sparkline pour alléger la réponse
        "price_change_percentage": "24h"     # Inclure explicitement la variation 24h
    }
    try:
        response = requests.get(COINGECKO_URL, params=params, timeout=5)  # Timeout 5 secondes
        if response.status_code == 200:
            data = response.json()
            # Tri côté Python par variation 24h décroissante
            top_movers = sorted(
                data,
                key=lambda x: x.get("price_change_percentage_24h") or 0,
                reverse=True
            )[:limit]
            logging.info(f"{len(top_movers)} top movers récupérés et triés sur {len(data)} cryptos.")
            return top_movers
        else:
            logging.warning(f"Réponse inattendue de l'API : {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        logging.error("Timeout : l'API CoinGecko ne répond pas.")
        return []
    except requests.exceptions.ConnectionError:
        logging.error("Erreur réseau : impossible de joindre l'API CoinGecko.")
        return []
    except Exception as e:
        logging.error(f"Erreur inattendue lors de l'appel API : {e}")
        return []