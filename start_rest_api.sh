#!/bin/bash
# Startup script for Google Keep REST API

cd /app
python -m uvicorn server.rest_api:app --host "${REST_API_HOST:-0.0.0.0}" --port "${REST_API_PORT:-8001}"
