#!/usr/bin/env python3
"""
Production server configuration for Stock King
"""

import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.api.main import app

# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for the HTML frontend)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main HTML file"""
    return FileResponse("simple_webpage.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "production_server:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
