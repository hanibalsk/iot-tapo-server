import nmap
import requests
from tapo import ApiClient
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class TapoNetworkScanner:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.scanner = nmap.PortScanner()

    async def scan_network(self, ip_range):
        logging.info(f"Scanning IP range: {ip_range}")
        self.scanner.scan(hosts=ip_range, arguments='-sn')  # -sn: Ping scan (no port scan)

        devices = []
        for host in self.scanner.all_hosts():
            if 'mac' in self.scanner[host]:
                mac_address = self.scanner[host]['addresses'].get('mac', 'Unknown')
            else:
                mac_address = 'Unknown'

            info = None
            ip_address = host
            if self.is_tapo_device_http(ip_address):
                logging.info(f"The device at {ip_address} is a Tapo device.")

                client = ApiClient(self.user, self.password)

                device = await client.generic_device(ip_address)
                info = await device.get_device_info()

                logging.info(f"Device info: {info.to_dict()}")
            else:
                logging.info(f"The device at {ip_address} is not a Tapo device.")

            devices.append({
                'ip': ip_address,
                'mac': mac_address,
                'state': self.scanner[host].state(),
                "device": info.to_dict() if info else None
            })

            logging.info(f"IP: {devices[-1]['ip']}, MAC: {devices[-1]['mac']}, State: {devices[-1]['state']}")

        return devices

    def is_tapo_device_http(self, ip):
        try:
            url = f"http://{ip}"
            response = requests.get(url, timeout=3)
            logging.info(f"Response headers for {ip}: {response.headers}")
            if "SHIP 2.0" in response.headers.get('Server', ''):
                return True
        except requests.RequestException:
            pass
        return False

