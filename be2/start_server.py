#!/usr/bin/env python3
"""
Startup script untuk AI-FRSS YOLO Detection Service
"""
import sys
import os
from pathlib import Path

# Set working directory dan Python path
app_dir = Path(__file__).parent / "app"
be2_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Load environment variables from be2/.env
from dotenv import load_dotenv
load_dotenv(be2_dir / ".env")

# Change to app directory for running
os.chdir(app_dir)

print("🚀 Starting AI-FRSS YOLO Detection Service...")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🔧 DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"🔧 PORT: {os.getenv('PORT')}")

# Import and run the application
if __name__ == "__main__":
    import uvicorn
    
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    if DEBUG:
        # Development mode with reload
        uvicorn.run(
            "main:app",  # Use import string for reload
            host="0.0.0.0",
            port=PORT,
            reload=True,
            log_level="info"
        )
    else:
        # Production mode
        from main import app
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=PORT,
            log_level="info"
        )
