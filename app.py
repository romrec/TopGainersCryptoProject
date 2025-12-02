import streamlit as st
import sqlite3
from top_movers import get_top_movers
from db import init_db, save_to_db
from logging_conf import log_access, log_error, RESPONSE_TIME, start_http_server
import time

# Initialize DB
init_db()

# Start Prometheus server for metrics
start_http_server(8000)

st.title("Top Movers Crypto")
st.write("Affichage des top gainer crypto avec stockage DB, monitoring et stats.")

log_access()  # Incremente log access

start_time = time.time()  # Temps de debut
movers = get_top_movers()  # Recup API
RESPONSE_TIME.observe(time.time() - start_time)  # Mesure temps API

# Afficher statistiques
st.header("📊 Statistiques et Supervision")
st.write("Données sauvegardées : ")
conn = sqlite3.connect('/app/data/crypto_data.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM top_movers")
count = cursor.fetchone()[0]
st.write(f"📖 Nombre d'enregistrements en base : {count}")

# Afficher dernières sauvegardes
st.subheader("💾 Dernières données sauvegardées")
# Requery for table
cursor2 = conn.cursor()
cursor2.execute("SELECT symbol, name, price, volume, change_24h, timestamp FROM top_movers ORDER BY timestamp DESC LIMIT 10")
rows = cursor2.fetchall()
cursor2.close()
conn.close()

if rows:
    st.table([{"Symbole": row[0], "Nom": row[1], "Prix": f"${row[2]:.4f}", "Volume": f"{row[3]:.0f}", "Changement 24h": f"{row[4]:.2f}%", "Timestamp":
row[5]} for row in rows])
else:
    st.write("Aucune donnée sauvegardée.")

st.write("🕒 Temps de réponse API : DEMO - 0.5s (avec Prometheus tracking)")
st.write("🚨 Logs récents : Démonstration - Accès réussi, données sauvegardées")

if movers:
    st.header("💰 Top 10 Gainers (données sauvegardées en DB)")
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
