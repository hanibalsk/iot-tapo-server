import asyncio
import json
import logging

from iot_database import IoTDeviceDatabase
from iot_scan import TapoNetworkScanner

logging.basicConfig(level=logging.INFO)


class Importer:
    def __init__(self, user, password, db_name="iot_devices.db"):
        self.user = user
        self.password = password
        self.scanner = TapoNetworkScanner(user, password)
        self.db = IoTDeviceDatabase(db_name)

    def import_devices(self, ip_range):
        logging.info(f"Starting import process for IP range: {ip_range}")
        devices = asyncio.run(self.scanner.scan_network(ip_range))

        for device in devices:
            if 'device' in device and device['device'] is not None:
                device_info = device['device']
                device_data = {
                    'ip': device.get('ip'),
                    'mac': device_info.get('mac'),
                    'state': device.get('state'),
                    'avatar': device_info.get('avatar'),
                    'device_id': device_info.get('device_id'),
                    'device_on': device_info.get('device_on'),
                    'fw_id': device_info.get('fw_id'),
                    'fw_ver': device_info.get('fw_ver'),
                    'has_set_location_info': device_info.get('has_set_location_info'),
                    'hw_id': device_info.get('hw_id'),
                    'hw_ver': device_info.get('hw_ver'),
                    'lang': device_info.get('lang'),
                    'latitude': device_info.get('latitude'),
                    'longitude': device_info.get('longitude'),
                    'model': device_info.get('model'),
                    'nickname': device_info.get('nickname'),
                    'oem_id': device_info.get('oem_id'),
                    'on_time': device_info.get('on_time'),
                    'region': device_info.get('region'),
                    'rssi': device_info.get('rssi'),
                    'signal_level': device_info.get('signal_level'),
                    'specs': device_info.get('specs'),
                    'ssid': device_info.get('ssid'),
                    'time_diff': device_info.get('time_diff'),
                    'device_type': device_info.get('type')
                }
                self.db.add_device(device_data)
                logging.info(f"Device {device_data['nickname']} at IP {device_data['ip']} added to the database.")
            else:
                logging.info(f"Device at IP {device['ip']} does not have detailed information to add to the database.")

    def generate_data_object(self):
        account_info = {
            "username": self.user,
            "password": self.password
        }

        devices = self.db.get_all_devices()
        devices_list = [
            {
                "name": device.nickname,
                "device_type": device.device_type,
                "ip_addr": device.ip
            }
            for device in devices
        ]

        data = {
            "account": account_info,
            "devices": devices_list
        }
        logging.info("Generated data object.")
        return data

    @staticmethod
    def store_json_from_object(data_object, path_to_json):
        try:
            with open(path_to_json, 'w') as json_file:
                json.dump(data_object, json_file, indent=4)
            logging.info(f"JSON file successfully stored at: {path_to_json}")
        except Exception as e:
            logging.error(f"Failed to store JSON file: {e}")
