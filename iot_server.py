import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask

from config_loader import load_config
from iot_blueprint import iot_blueprint
from iot_database import IoTDeviceDatabase
from iot_importer import Importer

# Create Flask application
app = Flask(__name__)

# Load configuration from the environment variable CONFIG_PATH or default to "config.yml"
config_path = os.getenv("CONFIG_PATH", "config.yaml")
config = load_config(config_path)

# Configure logging
log_file = config.get('log_file', '/data/server.log')

# Create logfile if it does not exist
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up logging to console and log file
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setLevel(logging.INFO)

# Define the logging format and add handlers to the logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Initialize database
db = IoTDeviceDatabase(config.get('database', 'iot_database.db'))

username = config.get('tapo', {}).get('username')
password = config.get('tapo', {}).get('password')

# Initialize importer
importer = Importer(user=username, password=password)

# Register the blueprint
app.register_blueprint(iot_blueprint, url_prefix='/api')

# Print all registered endpoints
with app.app_context():
    for rule in app.url_map.iter_rules():
        logging.info(f"Endpoint: {rule.endpoint}, URL: {rule}")

if __name__ == "__main__":
    # Set debug mode and port from environment variables
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 4667))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
