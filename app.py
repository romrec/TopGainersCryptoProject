import streamlit as st  # Interface
import sqlite3  # DB
from top_movers import get_top_movers  # Message
from db import init_db, save_to_db  # Init et save DB
from logging_conf import log_access, log_error, RESPONSE_TIME, start_http_server  # Logs et metrics
import time  # Timing

# Initialize DB
init_db()  # Init DB

# Start Prometheus server for metrics
start_http_server(8000)  # Démarre metrics server

st.title("Top Movers Crypto")  # Titre
st.write("Affichage des top gainer crypto avec stockage DB, monitoring et stats.")  # Desc

log_access()  # Log access

start_time = time.time()  # Debut timing
movers = get_top_movers()  # Recup données API
RESPONSE_TIME.observe(time.time() - start_time)  # Observe response time

# Afficher statistiques
st.header("📊 Statistiques et Supervision")  # Header stats
st.write("Données sauvegardées : ")  # Title section
conn = sqlite3.connect('/app/data/crypto_data.db')  # Connect DB
cursor = conn.cursor()  # Curseur
cursor.execute("SELECT COUNT(*) FROM top_movers")  # Count records
count = cursor.fetchone()[0]  # Get count
st.write(f"📖 Nombre d'enregistrements en base : {count}")  # Display count

# Afficher dernières sauvegardes
st.subheader("💾 Dernières données sauvegardées")  # Subheader
cursor2 = conn.cursor()  # Cursor2
cursor2.execute("SELECT symbol, name, price, volume, change_24h, timestamp FROM top_movers ORDER BY timestamp DESC LIMIT 10")  # Select last 10
rows = cursor2.fetchall()  # Fetch rows
cursor2.close()  # Close cursor
conn.close()  # Close conn

if rows:  # If data
    st.table([{"Symbole": row[0], "Nom": row[1], "Prix": f"${row[2]:.4f}", "Volume": f"{row[3]:.0f}", "Changement 24h": f"{row[4]:.2f}%", "Timestamp": row[5]} for row in rows])  # Table
else:
    st.write("Aucune donnée sauvegardée.")  # No data

st.write("🕒 Temps de réponse API : DEMO - 0.5s (avec Prometheus tracking)")  # Demo time
st.write("🚨 Logs récents : Démonstration - Accès réussi, données sauvegardées")  # Demo logs

if movers:  # If api data
    st.header("💰 Top 10 Gainers (données sauvegardées en DB)")  # Header
    for i, coin in enumerate(movers, 1):  # Loop coins
        symbol = coin['symbol'].upper()  # Get symbol
        name = coin['name']  # Get name
        price = coin['current_price']  # Get price
        volume = coin['total_volume']  # Get volume
        change = coin['price_change_percentage_24h']  # Get change

        # Save to DB
        save_to_db(symbol, name, price, volume, change)  # Persist

        color = "red" if change > 0 else "green"  # Color for change
        st.markdown(f"{i}. **{name} ({symbol})**: ${price:.4f}, Vol:{volume:.0f}, <span style='color:{color};'>(+{change:.2f}%)</span>", unsafe_allow_html=True)  # Display
else:
    st.write("Erreur : Impossible de récupérer les données depuis l'API.")  # Error UI
    log_error("Échec récupération données API")  # Log error
