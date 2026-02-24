import logging
from prometheus_client import start_http_server, Counter, Histogram

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[  # Handlers
        logging.FileHandler('/app/data/app.log'),  # Fichier log
        logging.StreamHandler()  # Console log
    ]
)

# Compteurs Prometheus
API_CALLS_TOTAL = Counter('api_calls_total', 'Nombre total d\'appels API', ['status'])  # Compteur d'appels API avec label status
DB_RECORDS_TOTAL = Counter('db_records_total', 'Nombre total d\'enregistrements en base')  # Compteur d'enregistrements en base

# Histogramme pour le temps de réponse de l'API
API_RESPONSE_SECONDS = Histogram('api_response_seconds', 'Temps de réponse de l\'API CoinGecko', buckets=[0.1, 0.5, 1, 2, 5, 10])

# Compteurs existants
ACCESS_COUNTER = Counter('app_requests_total', 'Nombre total de requêtes')  # Compteur requêtes
ERROR_COUNTER = Counter('app_errors_total', 'Nombre total d\'erreurs')  # Compteur erreurs
RESPONSE_TIME = Histogram('app_response_time_seconds', 'Temps de réponse', buckets=[0.1, 0.5, 1, 2, 5, 10])  # Histogramme temps

def log_access(): 
    ACCESS_COUNTER.inc() # Incremente compteur requêtes
    logging.info("Accès enregistré")
    
def log_error(msg):
    ERROR_COUNTER.inc()  # Incremente compteur erreurs
    logging.error(msg)

def log_api_call(status):
    """Enregistre un appel API avec son statut."""
    API_CALLS_TOTAL.labels(status=status).inc()
    logging.info(f"Appel API enregistré avec statut: {status}")

def log_api_response_time(duration):
    """Enregistre le temps de réponse de l'API."""
    API_RESPONSE_SECONDS.observe(duration)
    logging.info(f"Temps de réponse API: {duration:.2f}s")

def log_db_record():
    """Enregistre un enregistrement en base de données."""
    DB_RECORDS_TOTAL.inc()
    logging.info("Enregistrement en base de données effectué")