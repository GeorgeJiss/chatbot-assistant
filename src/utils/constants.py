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

# Greeting messages
GREETING_MESSAGE = """
👋 Hello! Welcome to **TalentScout AI Hiring Assistant**.

I'm here to help with your initial screening process for technology positions. 

I'll be asking you some questions to:
1. Gather your basic information
2. Understand your technical expertise
3. Assess your skills through relevant questions

This should take about 10-15 minutes. Let's get started!

**To begin, could you please tell me your full name?**

_(You can type 'exit' or 'quit' at any time to end the conversation)_
"""

# Information gathering prompts
INFO_PROMPTS = {
    InfoField.NAME: "Great! Could you please provide your full name?",
    InfoField.EMAIL: "Thank you! What's your email address?",
    InfoField.PHONE: "Perfect! What's your phone number?",
    InfoField.EXPERIENCE: "How many years of professional experience do you have?",
    InfoField.POSITION: "What position(s) are you interested in applying for?",
    InfoField.LOCATION: "Where are you currently located?",
    InfoField.TECH_STACK: """
Now, let's talk about your technical skills!

Please list your tech stack - the technologies you're proficient in. This can include:
- Programming languages (e.g., Python, JavaScript, Java)
- Frameworks (e.g., React, Django, Spring Boot)
- Databases (e.g., PostgreSQL, MongoDB)
- Tools (e.g., Docker, Git, AWS)

You can list them separated by commas.
"""
}

# Fallback responses
FALLBACK_RESPONSES = [
    "I didn't quite understand that. Could you please rephrase?",
    "I'm sorry, I'm having trouble understanding. Could you provide that information again?",
    "I couldn't process that response. Let's try again - could you please provide the requested information?",
]

# Closing message
CLOSING_MESSAGE = """
🎉 **Thank you for completing the screening process!**

We've successfully collected all your information and assessed your technical skills.

**Next Steps:**
1. Our recruitment team will review your responses within 2-3 business days
2. If your profile matches our requirements, we'll reach out via email or phone
3. You may be invited for a technical interview with our client companies

**What to expect:**
- Review timeline: 2-3 business days
- Technical interview: 45-60 minutes
- Final decision: 1 week after interview

We appreciate your time and interest in opportunities through TalentScout!

For any questions, feel free to reach out to us at careers@talentscout.com

Good luck! 🚀
"""

# Exit message
EXIT_MESSAGE = """
Thank you for your time! Your session has been saved.

If you'd like to continue later, please reach out to us at careers@talentscout.com

Have a great day! 👋
"""

# Technical question categories
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
    "lead": (10, float('inf'))
}