import streamlit as st
from api import get_top_movers
from db import init_db, save_to_db
from logging_conf import log_access, log_error, RESPONSE_TIME, start_http_server
import time

# Initialize DB
init_db()

# Start Prometheus server for metrics
start_http_server(8000)

st.title("Top Movers Crypto")
st.write("Affichage des top gainer crypto avec stockage DB et monitoring.")

log_access()

start_time = time.time()
movers = get_top_movers()
RESPONSE_TIME.observe(time.time() - start_time)

if movers:
    st.write("Top 10 Gainers (données sauvegardées en DB):")
    for i, coin in enumerate(movers, 1):
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        volume = coin['total_volume']
        change = coin['price_change_percentage_24h']
        color = "red" if change > 0 else "green"

        # Save to DB
        save_to_db(symbol, name, price, volume, change)

        st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f}, Vol:{volume:.0f}, <span style='color:{color};'>(+{change:.2f}%)</span>", unsafe_allow_html=True)
else:
    st.write("Impossible de récupérer les données.")
    log_error("Failed to fetch data from API")
