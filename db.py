import os
import logging
from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor

# Configuration de la base de données via variables d'environnement
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "crypto_data")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_PATH = None  # Plus utilisé — garde pour compatibilité mais plus de DB_PATH SQLite

logger = logging.getLogger(__name__)


def get_db_connection():
    """Obtient une connexion à la base de données PostgreSQL."""
    try:
        conn = connect(DB_URL, cursor_factory=RealDictCursor)
        return conn
    except OperationalError as e:
        logger.error(f"Erreur de connexion à la base de données : {e}")
        return None


def init_db():
    """Initialise la base de données PostgreSQL et crée la table top_movers si elle n'existe pas."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Impossible d'établir la connexion à la base de données.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS top_movers (
                id         SERIAL PRIMARY KEY,
                symbol     TEXT NOT NULL,
                name       TEXT NOT NULL,
                price      REAL NOT NULL,
                volume     REAL NOT NULL,
                change_24h REAL NOT NULL,
                timestamp  TIMESTAMPTZ DEFAULT NOW()
            )
        ''')
        conn.commit()
        logger.info("Base de données initialisée.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base : {e}")
    finally:
        conn.close()


def save_to_db(symbol, name, price, volume, change_24h):
    """Insère un enregistrement dans la table top_movers."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Impossible d'établir la connexion à la base de données.")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO top_movers (symbol, name, price, volume, change_24h)
               VALUES (%s, %s, %s, %s, %s)''',
            (symbol, name, price, volume, change_24h)
        )
        conn.commit()
        logger.info(f"Données sauvegardées pour {symbol}.")
        return True
    except Exception as e:
        logger.error(f"Erreur sauvegarde en DB: {e}")
        return False
    finally:
        conn.close()


def get_top_movers_from_db(limit=10):
    """Récupère les dernières entrées enregistrées en base."""
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT symbol, name, price, volume, change_24h, timestamp
               FROM top_movers
               ORDER BY timestamp DESC
               LIMIT %s''',
            (limit,)
        )
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"Erreur lecture en DB: {e}")
        return []
    finally:
        conn.close()


def get_latest_by_symbol(symbol):
    """Récupère la dernière entrée enregistrée pour un symbole donné."""
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT symbol, name, price, volume, change_24h, timestamp
               FROM top_movers
               WHERE symbol = %s
               ORDER BY timestamp DESC
               LIMIT 1''',
            (symbol,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Erreur lecture en DB pour {symbol}: {e}")
        return None
    finally:
        conn.close()
