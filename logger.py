import logging

# Configure logging
logging.basicConfig(
    filename='log.txt',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_error(error_message):
    """Log an error message to the log file."""
    logging.error(error_message) 