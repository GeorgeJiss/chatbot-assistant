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

# LLM Settings
MAX_TOKENS = 1024
TEMPERATURE = 0.7
TOP_P = 0.9

# Data Storage
DATA_DIR = BASE_DIR / "data"
CANDIDATES_DIR = DATA_DIR / "candidates"
TECH_STACKS_DIR = DATA_DIR / "tech_stacks"
AUDIO_DIR = DATA_DIR / "audio"

# Create directories if they don't exist
CANDIDATES_DIR.mkdir(parents=True, exist_ok=True)
TECH_STACKS_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Validation Patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'

# Question Generation - REDUCED FOR 15 MIN INTERVIEW
QUESTIONS_PER_TECH = 2  # Reduced from 3
MAX_TECH_STACK_ITEMS = 3  # Max 3 technologies
MIN_TECH_STACK_ITEMS = 1

# Voice Settings
VOICE_ENABLED = True
TTS_LANGUAGE = 'en'
TTS_SLOW = False
SPEECH_TIMEOUT = 30  # seconds to wait for answer
SPEECH_PHRASE_TIMEOUT = 5  # seconds of silence before stopping
ANSWER_WAIT_TIME = 45  # seconds to wait before prompting

# Interview Time Management
MAX_INTERVIEW_DURATION = 900  # 15 minutes in seconds
WARNING_TIME = 720  # 12 minutes - show warning

# Answer Quality Settings
MIN_ANSWER_LENGTH = 20  # characters
MAX_ANSWER_LENGTH = 1000  # characters
SENTIMENT_THRESHOLD = -0.3  # negative sentiment threshold

# Multilingual Support
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'zh-cn': 'Chinese'
}

# Session Settings
SESSION_TIMEOUT_MINUTES = 30

# Application Settings
APP_NAME = "TalentScout AI Voice Interviewer"
APP_VERSION = "2.0.0"
COMPANY_NAME = "TalentScout"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Create logs directory
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
