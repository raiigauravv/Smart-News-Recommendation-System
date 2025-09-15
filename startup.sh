#!/bin/bash

# Azure App Service startup script for FastAPI
cd /home/site/wwwroot/server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000