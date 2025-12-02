import sqlite3  # Import DB
import logging  # Import logging

DB_PATH = '/app/data/crypto_data.db'  # Path to DB in volume

def init_db():  # Init DB table
    conn = sqlite3.connect(DB_PATH)  # Connect DB
    cursor = conn.cursor()  # Create cursor
    cursor.execute('''  # Create table if not exists
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
    conn.commit()  # Save changes
    conn.close()  # Close conn
    logging.info("Base de données initialisée.")  # Log init

def save_to_db(symbol, name, price, volume, change_24h):  # Insert record
    try:
        conn = sqlite3.connect(DB_PATH)  # Connect DB
        cursor = conn.cursor()  # Cursor for exec
        cursor.execute('''  # Insert data
            INSERT INTO top_movers (symbol, name, price, volume, change_24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, price, volume, change_24h))  # Params
        conn.commit()  # Commit insert
        conn.close()  # Close conn
        logging.info(f"Sauvegardé {symbol} en DB.")  # Log save
    except Exception as e:  # Handle error
        logging.error(f"Erreur sauvegarde en DB: {e}")  # Log error
