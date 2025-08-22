# Backend Dockerfile (gateway único)
FROM python:3.11-slim

WORKDIR /app

# (Opcional) librerías nativas si más adelante usas mysqlclient;
# con PyMySQL no son necesarias, pero no molestan
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend (asegúrate de que aquí está server.py)
COPY . .

# Expones solo el puerto del gateway
EXPOSE 8000

# Arranca FastAPI gateway
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
