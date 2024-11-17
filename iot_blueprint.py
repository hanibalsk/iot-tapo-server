import logging

from flask import Blueprint, jsonify, request

logging.basicConfig(level=logging.INFO)

# Create a Flask Blueprint
iot_blueprint = Blueprint('iot', __name__)


# Endpoint to list all devices in the database
@iot_blueprint.route('/devices', methods=['GET'])
def list_devices():
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    filters = {}
    state = request.args.get('state')
    if state:
        filters['state'] = state

    from iot_server import db
    devices = db.get_all_devices(page=page, page_size=page_size, filters=filters)
    devices_list = [device.__dict__ for device in devices]
    for device in devices_list:
        device.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal state
    return jsonify(devices_list)


# Endpoint to import devices by scanning the network
@iot_blueprint.route('/import_devices', methods=['POST'])
def import_devices():
    data = request.get_json()
    ip_range = data.get('ip_range')
    if not ip_range:
        return jsonify({'error': 'ip_range is required'}), 400

    from iot_server import importer
    importer.import_devices(ip_range)
    return jsonify({'message': f'Devices from IP range {ip_range} imported successfully.'})
