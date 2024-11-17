# IoT Device Importer and Scanner

## Overview
The `Importer` class is a Python utility designed to scan a network for IoT devices using the TapoNetworkScanner and store the information in a local SQLite database. This tool can also generate device configuration in YAML format for further use.

## Features
- Scans the local network for IoT devices using Tapo API credentials.
- Stores device information in an SQLite database.
- Generates JSON or YAML configuration of devices for easy integration.
- Supports both importing devices into the database and exporting configuration.

## Requirements
- Python 3.7+
- `asyncio` for asynchronous operations
- `yaml` for exporting data to YAML format
- `sqlite3` via the `IoTDeviceDatabase` for device data storage
- Docker (optional for containerization)

## Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Ensure that your `requirements.txt` file includes packages such as `pyyaml`, `sqlite3`, etc.

# Docker Usage
A `Dockerfile` is provided to containerize the application for easier deployment.

## Building the Docker Image
To build the Docker image locally, use the `build.sh` script as follows:
```sh
./build.sh
```
This script builds the Docker image for multiple platforms, such as `amd64` and `arm64`, and optionally pushes it to a registry if specified.

Alternatively, you can manually build the Docker image:
```sh
docker build -t iot-device-importer .
```

## Running the Docker Container
To run the Docker container:
```sh
docker run -d -p 4667:4667     -e CONFIG_PATH=/data/config.yaml     -v /path/to/your/data:/data     -v /path/to/your/rest:/rest     iot-device-importer
```
- Replace `/path/to/your/data` and `/path/to/your/rest` with the actual paths on your host machine.

## Dockerfile Details
The `Dockerfile` included in this project is set up to create a lightweight container for the IoT Device Importer. It uses a `python:3.9-slim` base image to keep the container small and efficient.

### Key Dockerfile Commands
- **Base Image**: `python:3.9-slim` - A minimal Python image.
- **Working Directory**: `/app` - All files will be copied here.
- **Dependencies**: Requirements are installed using `pip` from `requirements.txt`.
- **Environment Variables**:
  - `FLASK_PORT`: The port that Flask listens on, default is `4667`.
  - `CONFIG_PATH`: Set to `/data/config.yaml`, allowing easy configuration changes.
  - `FLASK_ENV` and `FLASK_DEBUG` for production settings.
- **Volumes**: Two volumes are defined:
  - `/data`: For configuration and logging.
  - `/rest`: For storing REST configuration files.
- **Run Command**: Uses `gunicorn` to run the Flask server, ensuring production-level performance.

### Multi-Platform Build
The Dockerfile supports multi-platform builds. You can use the Docker `buildx` plugin to create images for multiple platforms (e.g., `amd64`, `arm64`).
Example build command:
```sh
docker buildx build --platform linux/amd64,linux/arm64 -t iot-device-importer:latest .
```

## Using Docker Compose
To simplify running multiple services, you can create a `docker-compose.yml` file. Here is an example to run the IoT Device Importer:

```yaml
version: '3.8'
services:
  iot-importer:
    image: iot-device-importer:latest
    ports:
      - "4667:4667"
    environment:
      CONFIG_PATH: /data/config.yaml
    volumes:
      - /path/to/your/data:/data
      - /path/to/your/rest:/rest
```
Run the application with:
```sh
docker-compose up -d
```

# Usage

## 1. Listing Devices from the Database
The server provides an API endpoint to list all devices stored in the database.

- **Endpoint**: `/api/devices`
- **Method**: `GET`
- **Query Parameters**:
  - `page` (optional, int): The page number for pagination (default is `1`).
  - `page_size` (optional, int): The number of devices per page (default is `10`).
  - `state` (optional, str): Filter devices by their state (e.g., `up`).

Example request:
```sh
curl -X GET "http://localhost:4667/api/devices?page=1&page_size=5"
```
This will return a paginated list of devices stored in the database.

## 2. Importing Devices by Scanning the Network
The server provides an API endpoint to import devices by scanning the network.

- **Endpoint**: `/api/import_devices`
- **Method**: `POST`
- **Request Body** (JSON):
  - `ip_range` (str): The IP range to scan (e.g., `192.168.0.0/24`).

Example request:
```sh
curl -X POST "http://localhost:4667/api/import_devices" -H "Content-Type: application/json" -d '{"ip_range": "192.168.0.0/24"}'
```
This will initiate a network scan and import detected devices into the database. If a `path_to_rest_config` is specified in the configuration, the scanned data will also be stored in a YAML file.

# Configuration Example
The Importer expects the following configuration:

```yaml
tapo:
  username: "<redacted>"  # Tapo account username (anonymized for security)
  password: "<redacted>"  # Tapo account password (anonymized for security)

database: "iot_devices.db"  # Path to the database file
log_file: "/data/server.log"  # Path to the log file

# https://github.com/hanibalsk/tapo-rest-crossplatform
path_to_rest_config: "/rest/config.yaml"  # Path to the REST configuration file (optional)
```

# API Methods

## `GET /api/devices`
Lists all devices in the database.
- **Query Parameters**:
  - `page` (optional, int): The page number for pagination.
  - `page_size` (optional, int): The number of devices per page.
  - `state` (optional, str): Filter devices by their state.
- **Returns**: A list of devices in the database.

## `POST /api/import_devices`
Imports devices by scanning the network.
- **Request Body** (JSON):
  - `ip_range` (str): The IP range to scan.
- **Returns**: A message indicating the import status.

# Logging
Logs are written to the log file specified in the configuration (`log_file`), with INFO-level logging used throughout the script to track progress and operations.

# License
This project is licensed under the MIT License. See the LICENSE file for more information.

# Contribution
Contributions are welcome! Please submit a pull request or open an issue for suggestions or improvements.

# TODO: Authentication
Currently, the API does not have any authentication mechanism. Implementing authentication is necessary to ensure that only authorized users can access and modify IoT device data. Possible approaches include:
- Token-based authentication (e.g., JWT).
- OAuth2 for more advanced use cases.
- Basic API key authentication.

# Disclaimer
The Tapo credentials (`username` and `password`) are sensitive. Always handle them securely and avoid hardcoding in public repositories.
