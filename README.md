# 🤖 TalentScout AI Hiring Assistant

An **intelligent, automated candidate screening assistant** built using **Streamlit** and powered by **Groq's Llama 3.1 LLM API**.  
TalentScout AI conducts structured interviews, validates candidate details, and dynamically generates technical questions tailored to the applicant’s experience and tech stack — all while ensuring data privacy and local storage.

---

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-API-00C853)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🧠 Overview

### What Is It?

**TalentScout AI Hiring Assistant** is a chatbot-powered application that simulates a **real-time HR screening and technical interview** process.  
It collects candidate details such as **name, email, phone, experience, preferred position, and tech stack**, and then generates **custom technical questions** per candidate profile.

### Why It Exists

Recruiters and HR teams often spend hours conducting repetitive screening rounds.  
This project automates that process — saving time while maintaining quality assessment.

### Highlights
- ⚙️ **Fully automated candidate screening**
- 🧑‍💻 **AI-generated technical questions**
- 🧩 **Dynamic difficulty adjustment** based on role/experience
- 🔒 **Data privacy first — local JSON storage only**
- 🧾 **Configurable interview logic & structure**
- 🚫 **Offline-capable — no cloud upload dependency**

---

## 🖼️ Demo Preview

### 👋 Interaction Example

🤖 Assistant: Hello! Welcome to TalentScout AI Hiring Assistant.
I'm here to conduct your initial screening interview.

You: John Smith
🤖 Assistant: Great! What’s your email address?
You: john.smith@email.com

🤖 Assistant: Perfect! What’s your tech stack?
You: Python, React, Docker, AWS
🤖 Assistant: Excellent! Let’s start your technical interview...


The chatbot dynamically tailors questions like:
> “Can you explain how Docker improves CI/CD pipelines?”  
> “Describe the role of React hooks in component lifecycle management.”

---

## 🧩 System Architecture

```mermaid
flowchart TD
    A[User Interface (Streamlit)] -->|Input| B[Chatbot Manager]
    B -->|Requests| C[Groq LLM API]
    B -->|Validation| D[Validation Service]
    B -->|Save Data| E[Storage Service]
    B -->|Question Logic| F[Question Generator]
    C -->|LLM Response| B
    E -->|Local JSON| G[data/candidates]

Core Flow:

User enters basic information

Validation Service checks input (email, phone, etc.)

Chatbot Manager orchestrates conversation and passes prompts to Groq API

Question Generator tailors technical questions based on tech stack + experience

Responses stored locally under /data/candidates/ for recruiter access

⚙️ Configuration
🧾 Environment Setup

Create a .env file in your project root:

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
LOG_LEVEL=INFO

🔑 Get a Free Groq API Key

Visit https://console.groq.com

Sign up using GitHub or Google

Generate an API key and paste it into .env

Free tier limits:

14,400 requests/day

600 requests/hour

Access to Llama 3.1, Mixtral, Gemma models

No credit card required

🛠️ Installation & Setup
1️⃣ Quick Setup (Linux/Mac)
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
chmod +x setup.sh
./setup.sh
streamlit run app.py

2️⃣ Manual Setup (All OS)
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
nano .env                       # Add your API key
streamlit run app.py


Access the app at http://localhost:8501

💡 Features Explained
Feature	Description
🗣️ Chat-based Interview	Interactive session with structured HR-style prompts
🧠 AI-Powered Assessment	Uses Groq’s Llama 3.1 70B to create dynamic technical questions
📊 Smart Difficulty Control	Adjusts question complexity based on experience or job title
✅ Input Validation	Built-in regex checks for email/phone formatting
💾 Local Data Storage	Stores all session data in /data/candidates/
⚡ Auto Save & Resume	Session state automatically saved and restorable
🔐 Privacy Focused	GDPR-friendly — no data sent to cloud except LLM prompt
🛑 Exit Anytime	Type exit, quit, or bye to end safely
🧱 Project Structure
talentscout-hiring-assistant/
│
├── app.py                  # Streamlit UI + main chat logic
├── config.py               # All app configuration & constants
├── setup.sh                # Automated setup script
├── requirements.txt        # Project dependencies
│
├── src/
│   ├── chatbot/
│   │   ├── manager.py              # Core conversation manager
│   │   └── conversation_flow.py    # Dialogue flow logic
│   │
│   ├── services/
│   │   ├── llm_service.py          # Groq API integration
│   │   ├── validation_service.py   # Input validation (regex)
│   │   └── storage_service.py      # JSON-based local storage
│   │
│   ├── prompts/
│   │   ├── system_prompts.py       # Base system instructions
│   │   └── question_generator.py   # Dynamic question logic
│   │
│   └── utils/
│       ├── constants.py            # Exit keywords & helper constants
│       └── helpers.py              # Utility functions
│
├── data/
│   ├── candidates/                 # Stored candidate sessions
│   └── tech_stacks/question_bank.json
│
└── logs/
    └── app.log                     # Runtime logs

🧩 Key Files Explained
app.py

Streamlit UI for chatbot interface

Manages user input, chat history, and visual layout

Uses custom CSS for a professional interview UI

config.py

Holds all application settings

Handles environment loading, directory creation, validation patterns

Defines question difficulty, storage structure, and role mappings

🧪 Testing

To run tests:

pytest tests/ -v


or with coverage:

pytest --cov=src tests/

☁️ Deployment
🌐 Streamlit Cloud (Free)

Push your repository to GitHub

Go to Streamlit Cloud

Connect your repo

Add this in the app’s “Secrets” section:

GROQ_API_KEY = "your_key"


Click Deploy

💻 Local Deployment
streamlit run app.py


Then open http://localhost:8501

🧠 Technical Details
Component	Description
Frontend	Streamlit 1.29.0
Backend	Python 3.9+
LLM Provider	Groq API (Llama 3.1 70B)
Storage	Local JSON files
Testing	pytest 7.4.3
🧩 Core Classes
Class	Responsibility
ChatbotManager	Orchestrates conversation and state handling
LLMService	Connects to Groq API, handles retries and responses
ValidationService	Validates candidate inputs
StorageService	Stores and retrieves session data
QuestionGenerator	Dynamically generates interview questions
🤝 Contributing

Contributions are welcome!
To contribute:

Fork this repo

Create a new branch (feature/my-feature)

Commit and push your changes

Submit a Pull Request 🎉

👨‍💻 Author

George Jiss
📧 Email

🌐 GitHub Profile

🙏 Acknowledgments

Groq
 — for lightning-fast LLM inference

Streamlit
 — for the simple yet powerful UI framework

Meta AI
 — for Llama 3 model family
