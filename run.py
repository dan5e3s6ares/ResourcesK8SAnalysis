#!/usr/bin/env python3
"""
Kubernetes Resource Analysis - Startup Script
"""
import uvicorn
import os

if __name__ == "__main__":
    # Set development mode flag
    os.environ.setdefault("DEV_MODE", "true")
    
    # For development only - reload is disabled in production
    reload = os.getenv("DEV_MODE", "false").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload
    )
