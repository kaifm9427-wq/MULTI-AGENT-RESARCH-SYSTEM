#!/usr/bin/env python3
"""
HuggingFace Spaces Entry Point for ResearchMind
This file is specifically configured for HF Spaces deployment
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the project root and backend path
project_root = Path(__file__).resolve().parent
backend_path = project_root / "backend"

# Add backend to Python path
sys.path.insert(0, str(backend_path))

logger.info(f"Project root: {project_root}")
logger.info(f"Backend path: {backend_path}")
logger.info(f"Python path: {sys.path[:3]}")

# Now import the app
try:
    logger.info("Importing FastAPI app from backend.server...")
    from server import app
    logger.info("✅ Successfully imported app")
except ImportError as e:
    logger.error(f"❌ Failed to import app: {e}")
    # Try changing to backend directory
    os.chdir(backend_path)
    logger.info(f"Changed directory to {backend_path}")
    from server import app
    logger.info("✅ Successfully imported app after directory change")

# Verify required environment variables for HF Spaces
logger.info("Checking environment variables...")
required_vars = {
    "GEMINI_API_KEY": "Google Gemini API Key",
    "TAVILY_API_KEY": "Tavily Search API Key"
}

missing_vars = []
for var_name, var_description in required_vars.items():
    if not os.getenv(var_name):
        missing_vars.append(f"{var_name} ({var_description})")
    else:
        logger.info(f"✅ {var_name} is set")

if missing_vars:
    logger.warning(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
    logger.warning("The app will still start but some features may not work properly")

# Check if running on HF Spaces
is_hf_space = os.getenv("SPACE_ID") is not None
logger.info(f"Running on HuggingFace Spaces: {is_hf_space}")

if __name__ == "__main__":
    import uvicorn
    
    # Detect port
    if is_hf_space:
        port = 7860
        logger.info("🚀 Running on HuggingFace Spaces (port 7860)")
    else:
        port = int(os.getenv("PORT", 8000))
        logger.info(f"🚀 Running locally (port {port})")
    
    logger.info(f"Starting Uvicorn server on 0.0.0.0:{port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
