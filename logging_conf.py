import logging
from prometheus_client import start_http_server, Counter, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/data/app.log'),
        logging.StreamHandler()
    ]
)

# Prometheus metrics
ACCESS_COUNTER = Counter('app_requests_total', 'Total number of requests')
ERROR_COUNTER = Counter('app_errors_total', 'Total number of errors')
RESPONSE_TIME = Histogram('app_response_time_seconds', 'Response time in seconds', buckets=[0.1, 0.5, 1, 2, 5, 10])

def log_access():
    ACCESS_COUNTER.inc()
    logging.info("Access logged")

def log_error(msg):
    ERROR_COUNTER.inc()
    logging.error(msg)
