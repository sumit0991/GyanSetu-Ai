import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Set up a logger to give you clear feedback in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Config")

# 1. Absolute Path Calculation (Risk-Free)
# This finds the actual root of your project by looking at this file's location
# Path: root_folder/.env
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# 2. Force Load the .env file
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    logger.info(f"✅ Success: Loaded .env from {ENV_PATH}")
else:
    logger.warning(f"⚠️ Warning: .env file NOT found at {ENV_PATH}. Ensure it is in the project root.")


class Settings:
    PROJECT_NAME: str = "Mini2 Exam Assistant"

    # Storage Paths (using the absolute root we found)
    DATA_DIR = os.path.join(str(BASE_DIR), "backend", "data")
    VECTOR_DB_DIR = os.path.join(DATA_DIR, "vector_store")
    RAW_PDF_DIR = os.path.join(DATA_DIR, "raw_pdfs")

    # --- LLM Configurations ---
    # UPDATED 2026: Switching to 'gemini-3-flash' to fix the 404 Error.
    # If gemini-3-flash is not yet in your region, use 'gemini-2.5-flash'.
    LLM_MODEL = "gemini-3-flash"

    # Pull the key from the environment after load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Local embedding model (remain local for speed and cost)
    EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # API Keys for external services
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "AIzaSyAgteCzMsOIvGX8R5cJzCYIC3p4iNSYRTc")


settings = Settings()

# 3. Critical Boot-up Validation
if not settings.GOOGLE_API_KEY:
    logger.error("❌ ERROR: GOOGLE_API_KEY is missing! Gemini will not work.")
else:
    # We only print the first 5 characters for security
    logger.info(f"🔑 API Key Detected: {settings.GOOGLE_API_KEY[:5]}...")

# Create necessary directories
for path in [settings.VECTOR_DB_DIR, settings.RAW_PDF_DIR]:
    os.makedirs(path, exist_ok=True)