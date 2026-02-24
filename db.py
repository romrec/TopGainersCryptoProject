import sqlite3
import logging

DB_PATH = 'data/crypto_data.db'  # Chemin vers la base de données


def init_db():
    """Initialise la base de données et crée la table top_movers si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS top_movers (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol     TEXT NOT NULL,       -- Symbole de la crypto (ex: BTC)
            name       TEXT NOT NULL,       -- Nom complet (ex: Bitcoin)
            price      REAL NOT NULL,       -- Prix en USD au moment de la collecte
            volume     REAL NOT NULL,       -- Volume d'échanges sur 24h
            change_24h REAL NOT NULL,       -- Variation en % sur 24h
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP  -- Date de collecte
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Base de données initialisée.")


def save_to_db(symbol, name, price, volume, change_24h):
    """Insère un enregistrement dans la table top_movers.
    
    Args:
        symbol     : Symbole boursier de la crypto (ex: 'BTC')
        name       : Nom complet de la crypto (ex: 'Bitcoin')
        price      : Prix en USD
        volume     : Volume d'échanges sur 24h
        change_24h : Variation en pourcentage sur 24h
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO top_movers (symbol, name, price, volume, change_24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (symbol, name, price, volume, change_24h))
        conn.commit()
        conn.close()
        logging.info(f"Données sauvegardées pour {symbol}.")
    except Exception as e:
        logging.error(f"Erreur sauvegarde en DB: {e}")


def get_top_movers_from_db(limit=10):
    """Récupère les dernières entrées enregistrées en base.
    
    Args:
        limit : Nombre maximum de résultats à retourner (défaut: 10)
    
    Returns:
        Liste de tuples (symbol, name, price, volume, change_24h, timestamp)
        ou liste vide en cas d'erreur.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symbol, name, price, volume, change_24h, timestamp
            FROM top_movers
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Erreur lecture en DB: {e}")
        return []


def get_latest_by_symbol(symbol):
    """Récupère la dernière entrée enregistrée pour un symbole donné.
    Utilisé pour le fallback en cas d'indisponibilité de l'API.
    
    Args:
        symbol : Symbole de la crypto (ex: 'BTC')
    
    Returns:
        Tuple (symbol, name, price, volume, change_24h, timestamp)
        ou None si aucune donnée disponible.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symbol, name, price, volume, change_24h, timestamp
            FROM top_movers
            WHERE symbol = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (symbol,))
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        logging.error(f"Erreur lecture en DB pour {symbol}: {e}")
        return None