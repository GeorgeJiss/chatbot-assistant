import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

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

# Question Generation - ROLE-BASED
QUESTIONS_PER_TECH = 3  # 3-5 questions per technology
MAX_TECH_STACK_ITEMS = 5  # Maximum 5 technologies
MIN_TECH_STACK_ITEMS = 1  # Minimum 1 technology

# Time Management
QUESTION_TIME_LIMIT = 120  # 2 minutes (120 seconds) per question
WARNING_TIME = 30  # Show warning at 30 seconds remaining

# Role-Based Question Difficulty
ROLE_DIFFICULTY_MAP = {
    # Junior roles
    'intern': 'junior',
    'junior': 'junior',
    'entry level': 'junior',
    'graduate': 'junior',
    'trainee': 'junior',
    
    # Mid-level roles
    'developer': 'mid',
    'engineer': 'mid',
    'mid level': 'mid',
    'software engineer': 'mid',
    
    # Senior roles
    'senior': 'senior',
    'lead': 'senior',
    'principal': 'senior',
    'staff': 'senior',
    
    # Architect/Lead roles
    'architect': 'architect',
    'tech lead': 'architect',
    'engineering manager': 'architect',
    'head': 'architect'
}

# Experience-Based Difficulty (fallback)
EXPERIENCE_DIFFICULTY = {
    (0, 2): 'junior',      # 0-2 years
    (2, 5): 'mid',         # 2-5 years
    (5, 10): 'senior',     # 5-10 years
    (10, 100): 'architect' # 10+ years
}

# Answer Quality Settings
MIN_ANSWER_LENGTH = 20  # Minimum 20 characters
MAX_ANSWER_LENGTH = 2000  # Maximum 2000 characters
SENTIMENT_THRESHOLD = -0.3  # Negative sentiment threshold

# Proctoring Settings
MAX_TAB_SWITCHES = 3  # Flag if more than 3 tab switches
COPY_PASTE_DISABLED = True  # Disable copy-paste

# Session Settings
SESSION_TIMEOUT_MINUTES = 30

# Application Settings
APP_NAME = "TalentScout AI Hiring Assistant"
APP_VERSION = "2.1.0"
COMPANY_NAME = "TalentScout"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Create logs directory
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Auto-save frequency
AUTO_SAVE_FREQUENCY = 1  # Save after every answer

# Technology Categories with subcategories
TECH_CATEGORIES = {
    "languages": {
        "web": ["javascript", "typescript", "html", "css"],
        "backend": ["python", "java", "c#", "go", "rust", "php", "ruby"],
        "mobile": ["swift", "kotlin", "dart"],
        "systems": ["c", "c++", "rust"],
        "data": ["python", "r", "sql", "scala"]
    },
    "frameworks": {
        "frontend": ["react", "angular", "vue", "svelte", "next.js", "nuxt"],
        "backend": ["django", "flask", "fastapi", "spring", "express", "nest.js", "laravel", "rails"],
        "mobile": ["react native", "flutter", "ionic"],
        "fullstack": ["next.js", "nuxt", "meteor"]
    },
    "databases": {
        "sql": ["postgresql", "mysql", "oracle", "sql server", "sqlite"],
        "nosql": ["mongodb", "cassandra", "couchdb"],
        "cache": ["redis", "memcached"],
        "search": ["elasticsearch", "solr"]
    },
    "cloud": {
        "aws": ["aws", "ec2", "s3", "lambda", "dynamodb", "rds"],
        "azure": ["azure", "azure functions", "cosmos db"],
        "gcp": ["gcp", "google cloud", "firestore", "cloud functions"],
        "platforms": ["heroku", "netlify", "vercel", "digitalocean"]
    },
    "devops": {
        "containers": ["docker", "kubernetes", "podman"],
        "ci_cd": ["jenkins", "gitlab ci", "github actions", "circleci"],
        "iac": ["terraform", "ansible", "cloudformation"],
        "monitoring": ["prometheus", "grafana", "datadog", "new relic"]
    },
    "tools": {
        "version_control": ["git", "github", "gitlab", "bitbucket"],
        "testing": ["jest", "pytest", "junit", "selenium", "cypress"],
        "build": ["webpack", "vite", "gradle", "maven"],
        "api": ["postman", "swagger", "graphql"]
    }
}