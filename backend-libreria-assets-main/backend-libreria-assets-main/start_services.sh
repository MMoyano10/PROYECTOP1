#!/bin/bash
set -e

# Start all FastAPI services in the background
uvicorn api_gateway.main:app --host 0.0.0.0 --port 8000 &
uvicorn assets_service.main:app --host 0.0.0.0 --port 8001 &
uvicorn assettags_service.main:app --host 0.0.0.0 --port 8002 &
uvicorn categories_service.main:app --host 0.0.0.0 --port 8003 &
uvicorn logs_service.main:app --host 0.0.0.0 --port 8004 &
uvicorn tags_service.main:app --host 0.0.0.0 --port 8005 &
uvicorn users_service.main:app --host 0.0.0.0 --port 8006 &

# Wait for all background jobs
wait 