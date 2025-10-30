import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Alternative models available on Groq
# - llama-3.1-70b-versatile (recommended)
# - mixtral-8x7b-32768
# - gemma2-9b-it

# LLM Settings
MAX_TOKENS = 1024
TEMPERATURE = 0.7
TOP_P = 0.9

# Data Storage
DATA_DIR = BASE_DIR / "data"
CANDIDATES_DIR = DATA_DIR / "candidates"
TECH_STACKS_DIR = DATA_DIR / "tech_stacks"

# Create directories if they don't exist
CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
TECH_STACKS_DIR.mkdir(parents=True, exist_ok=True)

# Validation Patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'

# Question Generation
QUESTIONS_PER_TECH = 3
MIN_TECH_STACK_ITEMS = 1
MAX_TECH_STACK_ITEMS = 10

# Session Settings
SESSION_TIMEOUT_MINUTES = 30

# Application Settings
APP_NAME = "TalentScout AI Hiring Assistant"
APP_VERSION = "1.0.0"
COMPANY_NAME = "TalentScout"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Create logs directory
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)