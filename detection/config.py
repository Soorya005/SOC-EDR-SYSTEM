import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Backend API Configuration
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")

# Ollama AI Configuration
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi4-mini")

# Sysmon Configuration
SYSMON_CHANNEL = "Microsoft-Windows-Sysmon/Operational"

# Sigma Rules Configuration
SIGMA_RULES_DIR = PROJECT_ROOT / "sigma-rules"

# Reporting Configuration
PDF_OUTPUT_DIR = BASE_DIR / "reports" / "output"

# Ensure output directories exist
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
