import sqlite3  # Import DB
import logging  # Import logging

DB_PATH = '/app/data/crypto_data.db' # chemin vers la DB

def init_db():  # Initialisation de la table
    conn = sqlite3.connect(DB_PATH)  # Connexion
    cursor = conn.cursor()  # Création du curseur
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS top_movers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT,
            price REAL NOT NULL,
            volume REAL,
            change_24h REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')  # Création de la table et exécution du curseur  
    conn.commit()  # Sauvegarde modifications
    conn.close()  # Fermeture connexion
    logging.info("Base de données initialisée.")

def save_to_db(symbol, name, price, volume, change_24h):  # Sauvegarde des données dans la DB
    try:
        conn = sqlite3.connect(DB_PATH)  #  # Connexion
        cursor = conn.cursor()  # Création du curseur
        cursor.execute('''
            INSERT INTO top_movers (symbol, name, price, volume, change_24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, price, volume, change_24h))
        conn.commit()  # Commit insert
        conn.close()  # Fermeture connexion
        logging.info(f"Sauvegardé {symbol} en DB.")  # Sauvegarde de symbole dans la DB
    except Exception as e:
        logging.error(f"Erreur sauvegarde en DB: {e}")
