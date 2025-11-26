import streamlit as st
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
        st.error(f"Erreur API: {response.status_code}")
        return []

st.title("Top Movers Crypto")
st.write("Utilisation de l'API CoinGecko pour afficher les crypto-monnaies les plus performantes en 24h.")

movers = get_top_movers()

if movers:
    st.write("Top 10 Gainers:")
    for i, coin in enumerate(movers, 1):
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        change = coin['price_change_percentage_24h']
        color = "red" if change > 0 else "green"
        st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f} <span style='color:{color};'>(+{change:.2f}%)</span>", unsafe_allow_html=True)
else:
    st.write("Impossible de récupérer les données.")
