import logging
import os

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
log_file = config.get('log_file', '/data/logging.log')

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
