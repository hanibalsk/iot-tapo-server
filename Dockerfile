# Use a lightweight base image for Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies, including nmap
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
ENV FLASK_PORT=4667
EXPOSE $FLASK_PORT

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV CONFIG_PATH="/data/config.yaml"

# Define a volume for /data to make it configurable
VOLUME ["/data"]
VOLUME ["/rest"]

# Command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:4667", "iot_server:app"]

# Multi-platform support for different architectures
# Example build command:
# docker buildx build --platform linux/amd64,linux/arm64 -t your-image-name:latest .