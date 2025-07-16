# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Make the start script executable
RUN chmod +x start_services.sh

EXPOSE 8000 8001 8002 8003 8004 8005 8006

CMD ["./start_services.sh"] 