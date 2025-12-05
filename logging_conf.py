import logging  # Logging module
from prometheus_client import start_http_server, Counter, Histogram  # Metrics

logging.basicConfig(  # Setup logging
    level=logging.INFO,  # Info level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format
    handlers=[  # Handlers
        logging.FileHandler('/app/data/app.log'),  # File log
        logging.StreamHandler()  # Console log
    ]
)

ACCESS_COUNTER = Counter('app_requests_total', 'Nombre total de requêtes')  # Compteur requêtes
ERROR_COUNTER = Counter('app_errors_total', 'Nombre total d\'erreurs')  # Compteur erreurs
RESPONSE_TIME = Histogram('app_response_time_seconds', 'Temps de réponse', buckets=[0.1, 0.5, 1, 2, 5, 10])  # Histogramme temps

def log_access():  # Increment access
    ACCESS_COUNTER.inc()  # Inc counter
    logging.info("Accès enregistré")  # Log info

def log_error(msg):  # Increment error
    ERROR_COUNTER.inc()  # Inc counter
    logging.error(msg)  # Log error
