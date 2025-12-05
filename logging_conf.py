import logging  # Logging module
from prometheus_client import start_http_server, Counter, Histogram

logging.basicConfig(  # Setup logging
    level=logging.INFO,  # Niveau info
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format
    handlers=[  # Handlers
        logging.FileHandler('/app/data/app.log'),  # Fichier log
        logging.StreamHandler()  # Console log
    ]
)

ACCESS_COUNTER = Counter('app_requests_total', 'Nombre total de requêtes')  # Compteur requêtes
ERROR_COUNTER = Counter('app_errors_total', 'Nombre total d\'erreurs')  # Compteur erreurs
RESPONSE_TIME = Histogram('app_response_time_seconds', 'Temps de réponse', buckets=[0.1, 0.5, 1, 2, 5, 10])  # Histogramme temps

def log_access(): 
    ACCESS_COUNTER.inc() # Incremente compteur requêtes
    logging.info("Accès enregistré")
    
def log_error(msg):
    ERROR_COUNTER.inc()  # Incremente compteur erreurs
    logging.error(msg)
