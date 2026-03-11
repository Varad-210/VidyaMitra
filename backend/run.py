#!/usr/bin/env python3
"""
VidyaMitra Backend Startup Script
"""

import uvicorn
import os
from pathlib import Path

def main():
    # Ensure uploads directory exists
    uploads_dir = Path("uploads/resumes")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Using default configuration.")
        print("   Copy .env.example to .env and configure as needed.")
    
    # Start the server
    print("🚀 Starting VidyaMitra Backend API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🌐 Server running on: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
