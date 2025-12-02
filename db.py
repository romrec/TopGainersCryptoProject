import sqlite3  # Import DB
import logging  # Import logging

DB_PATH = '/app/data/crypto_data.db' # chemin vers la DB

def init_db():  # Initialisation de la table
    conn = sqlite3.connect(DB_PATH)  # Connexion
    cursor = conn.cursor()  # Création et exécution
    cursor.execute('''  # Créer table si inexistante
        CREATE TABLE IF NOT EXISTS top_movers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT,
            price REAL NOT NULL,
            volume REAL,
            change_24h REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()  # Sauvegarde modifications
    conn.close()  # Fermeture connexion
    logging.info("Base de données initialisée.")

def save_to_db(symbol, name, price, volume, change_24h):  # Sauvegarde des données dans la DB
    try:
        conn = sqlite3.connect(DB_PATH)  #  # Connexion
        cursor = conn.cursor()  # Création cursor
        cursor.execute('''  # Insert data
            INSERT INTO top_movers (symbol, name, price, volume, change_24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, price, volume, change_24h))  # Params
        conn.commit()  # Commit insert
        conn.close()  # Close conn
        logging.info(f"Sauvegardé {symbol} en DB.")  # Log save
    except Exception as e:  # Handle error
        logging.error(f"Erreur sauvegarde en DB: {e}")  # Log error
