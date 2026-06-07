"""
Environnement de test — utilise des données mockées au lieu de l'API CoinGecko.
"""
import streamlit as st
import sqlite3
import time
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import init_db, save_to_db, get_top_movers_from_db, DB_PATH
from logging_conf import log_access, RESPONSE_TIME

# Base de test séparée
TEST_DB_PATH = 'data/test.db'
import db as db_module
db_module.DB_PATH = TEST_DB_PATH

# Données mockées
MOCK_MOVERS = [
    {"symbol": "btc", "name": "Bitcoin", "current_price": 67500.0, "total_volume": 28_500_000_000, "price_change_percentage_24h": 4.2},
    {"symbol": "eth", "name": "Ethereum", "current_price": 3450.0, "total_volume": 15_200_000_000, "price_change_percentage_24h": 6.8},
    {"symbol": "sol", "name": "Solana", "current_price": 148.0, "total_volume": 4_800_000_000, "price_change_percentage_24h": 12.5},
    {"symbol": "ada", "name": "Cardano", "current_price": 0.62, "total_volume": 1_200_000_000, "price_change_percentage_24h": 8.3},
    {"symbol": "dot", "name": "Polkadot", "current_price": 7.85, "total_volume": 850_000_000, "price_change_percentage_24h": 5.1},
    {"symbol": "avax", "name": "Avalanche", "current_price": 38.20, "total_volume": 1_100_000_000, "price_change_percentage_24h": 9.7},
    {"symbol": "link", "name": "Chainlink", "current_price": 16.40, "total_volume": 950_000_000, "price_change_percentage_24h": 7.4},
    {"symbol": "matic", "name": "Polygon", "current_price": 0.72, "total_volume": 620_000_000, "price_change_percentage_24h": 3.9},
    {"symbol": "atom", "name": "Cosmos", "current_price": 9.15, "total_volume": 480_000_000, "price_change_percentage_24h": 2.8},
    {"symbol": "fil", "name": "Filecoin", "current_price": 6.30, "total_volume": 380_000_000, "price_change_percentage_24h": 15.2},
]

init_db()

# Prometheus sur port 8000 (inchangé)
from prometheus_client import start_http_server as prom_start
try:
    prom_start(8000)
    logging.info("[TEST] Serveur Prometheus démarré sur le port 8000")
except OSError as e:
    logging.warning(f"[TEST] Impossible démarrer Prometheus : {e}")

st.title("🧪 Top Movers Crypto — ENVIRONNEMENT DE TEST")
st.write("Données mockées — aucun appel API réel effectué.")

log_access()

start_time = time.time()
time.sleep(0.1)
movers = MOCK_MOVERS
api_duration = time.time() - start_time
RESPONSE_TIME.observe(api_duration)

st.success("✅ API mockée — données factices utilisées")

session_records = 0
for coin in movers:
    symbol = coin['symbol'].upper()
    name = coin['name']
    price = coin['current_price']
    volume = coin['total_volume']
    change = coin['price_change_percentage_24h']
    save_to_db(symbol, name, price, volume, change)
    session_records += 1

logging.info(f"[TEST] Session : {session_records} enregistrements sauvegardés en DB test")

conn_stats = sqlite3.connect(TEST_DB_PATH)
cursor_stats = conn_stats.cursor()
cursor_stats.execute("SELECT COUNT(*) FROM top_movers")
total_count = cursor_stats.fetchone()[0]

st.header("📊 Statistiques et Supervision")
st.metric("📖 Enregistrements cette session", f"{session_records}")
st.metric("📚 Total en base (toutes sessions)", f"{total_count}")

st.subheader("💾 Dernières 10 données sauvegardées")
cursor2 = conn_stats.cursor()
cursor2.execute("SELECT symbol, name, price, volume, change_24h, timestamp FROM top_movers ORDER BY timestamp DESC LIMIT 10")
rows = cursor2.fetchall()
cursor2.close()
conn_stats.close()

if rows:
    import pandas as pd
    data = [{"Symbole": row[0], "Nom": row[1], "Prix": f"${row[2]:.4f}", "Volume": f"{row[3]:.0f}", "Changement 24h": f"{row[4]:.2f}%", "Timestamp": row[5]} for row in rows]
    df = pd.DataFrame(data, index=range(1, len(rows)+1))
    df.index.name = "#"
    st.table(df)
else:
    st.write("Aucune donnée sauvegardée.")

st.write(f"🕒 Temps de réponse simulé : {api_duration:.2f}s")
st.write(f"🔢 Enregistrements DB (cette session) : {session_records} — Total cumulé : {total_count}")

st.header("💰 Top 10 Gainers (données mockées)")
for i, coin in enumerate(movers, 1):
    symbol = coin['symbol'].upper()
    name = coin['name']
    price = coin['current_price']
    volume = coin['total_volume']
    change = coin['price_change_percentage_24h']
    color = "green" if change > 0 else "red"
    st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f}, Vol:{volume:.0f}, <span style='color:{color};'>(+{change:.2f}%)</span>", unsafe_allow_html=True)