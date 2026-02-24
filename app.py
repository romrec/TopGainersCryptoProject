import streamlit as st
import sqlite3
from top_movers import get_top_movers
from db import init_db, save_to_db, get_top_movers_from_db
from logging_conf import log_access, log_error, RESPONSE_TIME, start_http_server, log_api_call, log_api_response_time, log_db_record
import time
import logging

# Initialize DB
init_db()

# Start Prometheus server
try:
    start_http_server(8000)
    logging.info("Serveur Prometheus démarré sur le port 8000")
except OSError as e:
    logging.warning(f"Impossible démarrer serveur Prometheus : {e}")

st.title("Top Movers Crypto")
st.write("Affichage des top gainer crypto avec stockage DB, monitoring et stats.")

log_access()

start_time = time.time()
movers = get_top_movers()
api_duration = time.time() - start_time
RESPONSE_TIME.observe(api_duration)
log_api_response_time(api_duration)

# Enregistrer l'appel API avec son statut
if movers:
    log_api_call('success')
    api_disponible = True
else:
    log_api_call('error')
    api_disponible = False

# Fallback sur la base de données si l'API est indisponible
if not api_disponible:
    logging.warning("API CoinGecko indisponible, fallback sur les dernières données en base.")
    movers_db = get_top_movers_from_db()
    if movers_db:
        st.warning("⚠️ API indisponible — affichage des dernières données enregistrées.")
    else:
        st.error("❌ API indisponible et aucune donnée en base.")

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
cursor2 = conn.cursor()
cursor2.execute("SELECT symbol, name, price, volume, change_24h, timestamp FROM top_movers ORDER BY timestamp DESC LIMIT 10")
rows = cursor2.fetchall()
cursor2.close()
conn.close()

if rows:
    st.table([{"Symbole": row[0], "Nom": row[1], "Prix": f"${row[2]:.4f}", "Volume": f"{row[3]:.0f}", "Changement 24h": f"{row[4]:.2f}%", "Timestamp": row[5]} for row in rows])
else:
    st.write("Aucune donnée sauvegardée.")

st.write(f"🕒 Temps de réponse API : {api_duration:.2f}s")
st.write("🚨 Logs récents : Démonstration - Accès réussi, données sauvegardées")

# Afficher top movers et sauvegarder en DB
if api_disponible and movers:
    st.header("💰 Top 10 Gainers (données sauvegardées en DB)")
    for i, coin in enumerate(movers, 1):
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        volume = coin['total_volume']
        change = coin['price_change_percentage_24h']
        color = "green" if change > 0 else "red"

        # Sauvegarder en DB
        save_to_db(symbol, name, price, volume, change)
        log_db_record()

        st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f}, Vol:{volume:.0f}, <span style='color:{color};'>(+{change:.2f}%)</span>", unsafe_allow_html=True)
    
    # Vérification que ce sont bien les top 10 gainers
    st.write(f"✅ Vérification : Affichage des {len(movers)} crypto-monnaies avec la meilleure variation sur 24h")
    if len(movers) > 0:
        st.write(f"📈 Meilleur gain : {movers[0]['name']} ({movers[0]['symbol'].upper()}) avec +{movers[0]['price_change_percentage_24h']:.2f}%")

elif not api_disponible and movers_db:
    st.header("💰 Top 10 Gainers (dernières données connues)")
    for i, row in enumerate(movers_db, 1):
        symbol, name, price, volume, change, timestamp = row
        color = "green" if change > 0 else "red"
        st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f}, Vol:{volume:.0f}, <span style='color:{color};'>(+{change:.2f}%)</span> — <small>données du {timestamp}</small>", unsafe_allow_html=True)

else:
    st.write("Impossible de récupérer les données.")
    log_error("Échec récupération données API et base de données vide")