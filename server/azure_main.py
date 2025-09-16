#!/usr/bin/env python3
"""
Azure-specific entry point for Smart News Recommendation System
"""
import os
import sys
import uvicorn

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Azure expects the app to run on port 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Import the FastAPI app
    from app.main import app
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )