import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Latest model

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

# Question Generation - OPTIMIZED FOR 15 MIN INTERVIEW
QUESTIONS_PER_TECH = 2  # 2 questions per technology
MAX_TECH_STACK_ITEMS = 3  # Maximum 3 technologies
MIN_TECH_STACK_ITEMS = 1  # Minimum 1 technology

# Voice Settings - IMPROVED
VOICE_ENABLED = True
TTS_LANGUAGE = 'en'
TTS_SLOW = False
SPEECH_TIMEOUT = 20  # Reduced to 20 seconds to wait for answer start
SPEECH_PHRASE_TIMEOUT = 15  # Reduced to 15 seconds for complete answer
ANSWER_WAIT_TIME = 30  # 30 seconds to wait before prompting

# Interview Time Management - STRICT TIMING
MAX_INTERVIEW_DURATION = 900  # 15 minutes in seconds (900)
WARNING_TIME = 180  # Show warning at 3 minutes remaining (180)

# Answer Quality Settings
MIN_ANSWER_LENGTH = 10  # Minimum 10 characters (reduced for voice)
MAX_ANSWER_LENGTH = 1000  # Maximum 1000 characters
SENTIMENT_THRESHOLD = -0.3  # Negative sentiment threshold

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

# Auto-save frequency (in number of questions)
AUTO_SAVE_FREQUENCY = 1  # Save after every question

# UI Settings
ENABLE_CHAT_HISTORY = True  # Show chat history option
ENABLE_VOICE_MODE_TOGGLE = True  # Allow switching between voice and text
SHOW_PROGRESS_BAR = False  # Don't show progress to candidate (internal only)

# Admin Settings (for viewing results - not shown to candidates)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Change this!
SHOW_SCORES_TO_ADMIN_ONLY = True  # Only admin can see scores