from enum import Enum

class ConversationStage(Enum):
    """Conversation stages"""
    GREETING = "greeting"
    INFO_GATHERING = "info_gathering"
    TECH_STACK = "tech_stack"
    TECHNICAL_QUESTIONS = "technical_questions"
    CLOSING = "closing"

class InfoField(Enum):
    """Information fields to collect"""
    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    EXPERIENCE = "experience"
    POSITION = "position"
    LOCATION = "location"
    TECH_STACK = "tech_stack"

# Exit keywords
EXIT_KEYWORDS = [
    "exit", "quit", "bye", "goodbye", "stop", 
    "end", "close", "terminate", "leave"
]

# Greeting message
GREETING_MESSAGE = """Hello! Welcome to TalentScout AI Hiring Assistant.

I'm here to conduct your initial screening interview for technology positions.

The interview will take approximately 10-15 minutes. I'll ask you questions about:
• Your basic information
• Your technical expertise
• Your skills through relevant questions

You can type "exit", "quit", or "bye" at any time to end the interview.

**Let's start by entering your full name.**"""

# Information gathering prompts
INFO_PROMPTS = {
    InfoField.NAME: "Please tell me your full name.",
    InfoField.EMAIL: "What is your email address?",
    InfoField.PHONE: "What is your phone number?",
    InfoField.EXPERIENCE: "How many years of professional experience do you have? (e.g., '3 years', '5.5 years')",
    InfoField.POSITION: "What position are you interested in applying for?",
    InfoField.LOCATION: "Where are you currently located? (City, State/Country)",
    InfoField.TECH_STACK: """Please tell me your tech stack - the technologies you're proficient in.

List the technologies separated by commas. For example:
- Programming languages (Python, JavaScript, Java, etc.)
- Frameworks (React, Django, Spring, etc.)
- Databases (PostgreSQL, MongoDB, etc.)
- Tools (Docker, AWS, Git, etc.)

You can list up to 5 technologies."""
}

# Fallback responses
FALLBACK_RESPONSES = [
    "I didn't quite understand that. Could you please rephrase?",
    "I'm sorry, I'm having trouble understanding. Could you provide that information again?",
    "I couldn't process that response. Let's try again.",
]

# Closing message
CLOSING_MESSAGE = """🎉 Thank you for completing the screening interview!

We've successfully collected all your information and assessed your technical skills.

**Next Steps:**
1. Our recruitment team will review your responses within 2-3 business days
2. If your profile matches our requirements, we'll reach out via email or phone
3. You may be invited for a technical interview

**What to expect:**
• Review timeline: 2-3 business days
• Technical interview: 45-60 minutes (if selected)
• Final decision: 1 week after interview

We appreciate your time and interest in opportunities through TalentScout.

For questions, contact us at careers@talentscout.com

Good luck! 🚀"""

# Technical question categories - for question generation context
TECH_CATEGORIES = {
    "languages": [
        "python", "javascript", "java", "c++", "c#", "go", "rust", 
        "ruby", "php", "swift", "kotlin", "typescript", "scala"
    ],
    "frameworks": [
        "react", "angular", "vue", "django", "flask", "fastapi", 
        "spring", "express", "nest", "laravel", "rails", "next", 
        "nuxt", "svelte", "asp.net"
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch", 
        "cassandra", "oracle", "sql server", "dynamodb", "firestore"
    ],
    "cloud": [
        "aws", "azure", "gcp", "heroku", "digitalocean", 
        "vercel", "netlify", "cloudflare"
    ],
    "devops": [
        "docker", "kubernetes", "jenkins", "gitlab ci", "github actions",
        "terraform", "ansible", "prometheus", "grafana"
    ],
    "tools": [
        "git", "jira", "confluence", "postman", "swagger", 
        "webpack", "vite", "babel", "jest", "pytest"
    ]
}

# Experience levels
EXPERIENCE_LEVELS = {
    "junior": (0, 2),
    "mid": (2, 5),
    "senior": (5, 10),
    "architect": (10, float('inf'))
}