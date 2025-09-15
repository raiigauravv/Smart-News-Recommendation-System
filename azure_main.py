#!/usr/bin/env python3
import sys
import os

# Add the server directory to Python path
sys.path.insert(0, '/home/site/wwwroot/server')
sys.path.insert(0, '/home/site/wwwroot')

# Change to the server directory
os.chdir('/home/site/wwwroot/server')

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)