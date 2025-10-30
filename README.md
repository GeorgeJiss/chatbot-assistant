# 🤖 TalentScout AI Hiring Assistant

An intelligent chatbot for automated candidate screening and technical assessment, built with Streamlit and powered by Groq's LLM API.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-API-green)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Testing](#testing)
- [Contributing](#contributing)

## 🎯 Overview

TalentScout AI Hiring Assistant is a conversational AI system designed to streamline the initial screening process for technology recruitment. It conducts structured interviews with candidates, gathering essential information and assessing technical proficiency through dynamically generated questions tailored to each candidate's tech stack.

### Key Features

✅ **Automated Information Collection**
- Name, email, phone, experience
- Position, location, tech stack

✅ **Dynamic Question Generation**
- 3-5 questions per technology
- Difficulty based on experience
- Powered by Llama 3.1 70B

✅ **Smart Validation**
- Email format checking
- Phone number validation
- Experience parsing

✅ **Data Privacy**
- Local storage only
- GDPR compliant
- No cloud uploads

✅ **Exit Anytime**
- Type: exit, quit, bye
- Progress automatically saved

## 🚀 Installation

### Prerequisites

- Python 3.9+
- pip
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# Run automated setup
chmod +x setup.sh
./setup.sh

# Edit .env with your API key
nano .env

# Run the application
streamlit run app.py
```

### Manual Installation
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Create directories
mkdir -p data/candidates data/tech_stacks logs

# 6. Run application
streamlit run app.py
```

## ⚙️ Configuration

### Getting Groq API Key (FREE)

1. Visit https://console.groq.com/
2. Sign up using GitHub or Google
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy the key to your `.env` file

**Free Tier Benefits:**
- 14,400 requests per day
- 600 requests per hour
- No credit card required
- Access to Llama 3.1, Mixtral, and Gemma models

### Environment Variables

Create a `.env` file in the project root:
```env
# Required: Your Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model selection (default: llama-3.1-70b-versatile)
GROQ_MODEL=llama-3.1-70b-versatile

# Optional: Logging level (default: INFO)
LOG_LEVEL=INFO
```

## 📖 Usage

### Starting a Session

1. Run: `streamlit run app.py`
2. Open browser at `http://localhost:8501`
3. Follow the chatbot prompts
4. Provide your information
5. Answer technical questions
6. Complete the screening

### Example Conversation
```
Bot: Welcome! To begin, could you please tell me your full name?
You: John Smith

Bot: Great! What's your email address?
You: john.smith@email.com

Bot: Perfect! What's your phone number?
You: +1-555-123-4567

Bot: How many years of professional experience do you have?
You: 5 years

Bot: What position(s) are you interested in?
You: Senior Software Engineer

Bot: Where are you currently located?
You: San Francisco, CA

Bot: Please list your tech stack (comma-separated):
You: Python, React, PostgreSQL, Docker, AWS

Bot: Excellent! Now I'll ask you 15 technical questions...
```

## 📁 Project Structure
```
talentscout-hiring-assistant/
│
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── requirements.txt         # Dependencies
├── config.py               # Configuration
├── app.py                  # Main Streamlit app
├── setup.sh                # Setup script
│
├── src/
│   ├── __init__.py
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── manager.py              # Main chatbot logic
│   │   └── conversation_flow.py   # Flow controller
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py         # Groq API
│   │   ├── validation_service.py  # Input validation
│   │   └── storage_service.py     # Data storage
│   │
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── system_prompts.py      # System prompts
│   │   └── question_generator.py  # Question generation
│   │
│   └── utils/
│       ├── __init__.py
│       ├── constants.py           # Constants
│       └── helpers.py             # Helper functions
│
├── data/
│   ├── candidates/                # Candidate data
│   └── tech_stacks/
│       └── question_bank.json    # Question templates
│
├── tests/
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_llm_service.py
│   └── test_chatbot.py
│
└── logs/
    └── app.log                    # Application logs
```

## 🧪 Testing

Run the test suite:
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_validation.py -v
```

## 🚀 Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit https://share.streamlit.io/
3. Connect your repository
4. Add secrets in dashboard:
```toml
   GROQ_API_KEY = "your_key"
```
5. Deploy!

### Local Deployment
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

## 📊 Technical Details

### Technology Stack

- **Frontend**: Streamlit 1.29.0
- **Language**: Python 3.9+
- **LLM Provider**: Groq API (Llama 3.1 70B)
- **Storage**: JSON files (local)
- **Testing**: pytest 7.4.3

### Key Components

1. **ChatbotManager** - Orchestrates conversation flow
2. **LLMService** - Groq API integration with retry logic
3. **ValidationService** - Input validation (email, phone, etc.)
4. **StorageService** - JSON-based data persistence
5. **QuestionGenerator** - Dynamic technical question generation

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Your Name** - Initial work

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for free, fast LLM inference
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Meta AI](https://ai.meta.com/) for Llama models

## 📞 Contact

- Email: careers@talentscout.com
- GitHub: https://github.com/yourusername/talentscout-hiring-assistant

---

**Made with ❤️ for better hiring experiences**

*Last Updated: October 30, 2025*