import sqlite3
import logging

DB_PATH = '/app/data/crypto_data.db'

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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
    ''')
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def save_to_db(symbol, name, price, volume, change_24h):
    """Save a record to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO top_movers (symbol, name, price, volume, change_24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, price, volume, change_24h))
        conn.commit()
        conn.close()
        logging.info(f"Saved {symbol} to DB.")
    except Exception as e:
        logging.error(f"Error saving to DB: {e}")
