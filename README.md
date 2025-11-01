# 🤖 TalentScout AI Hiring Assistant

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](https://interview-assistant-chatbot.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)

> An intelligent AI-powered chatbot for automated technical candidate screening and assessment.

**🔗 Live Demo:** [https://interview-assistant-chatbot.streamlit.app/](https://interview-assistant-chatbot.streamlit.app/)

---

## 📝 What is This?

TalentScout is an **AI hiring assistant** that conducts structured technical interviews with candidates. It autonomously handles the initial screening process by:

- Collecting candidate information (name, email, experience, tech stack)
- Generating role-specific technical questions based on the candidate's expertise
- Adapting question difficulty based on experience level (Junior/Mid/Senior/Architect)
- Analyzing answer quality using sentiment analysis
- Saving interview data for recruiter review

Think of it as a **24/7 first-round technical screener** that provides consistent, unbiased candidate evaluation.

---

## 🎯 Why This Tech Stack?

| Technology | Purpose | Justification |
|------------|---------|---------------|
| **Streamlit** | Frontend Framework | Enables rapid development of interactive web apps with Python. Perfect for ML/AI demos with minimal frontend code. Built-in deployment to Streamlit Cloud. |
| **Groq API** | LLM Inference Engine | Provides ultra-fast inference speeds (10x faster than GPT-4) with their LPU™ architecture. Free tier available with generous rate limits (14,400 requests/day). |
| **Llama 3.3 70B** | Language Model | Meta's latest open-source model with superior reasoning capabilities. Excellent at generating contextual technical questions and understanding candidate responses. |
| **TextBlob** | NLP & Sentiment Analysis | Lightweight Python library for text processing. Provides quick sentiment scoring without heavy ML models. |
| **Python 3.9+** | Backend Language | Industry standard for AI/ML applications. Rich ecosystem of libraries and seamless integration with LLM APIs. |
| **JSON Storage** | Data Persistence | Simple, human-readable storage format. No database setup required. Easy for recruiters to review candidate data. |

### Key Design Decisions:

**1. Text-Only Interface**
- More accessible than voice (works everywhere, no microphone issues)
- Easier to review and analyze responses
- Reduces technical barriers for candidates

**2. Groq over OpenAI**
- 10x faster response times (better user experience)
- Free tier sufficient for MVP
- Same API structure, easy to switch later

**3. Role-Based Question Generation**
- Junior candidates get fundamental questions
- Senior candidates get architecture/design questions
- Prevents frustration and provides fair assessment

**4. Modular Architecture**
- Separation of concerns (services, prompts, utils)
- Easy to add features (video, scoring, proctoring)
- Maintainable and testable code

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────┐
│                     Streamlit UI                        │
│                      (app.py)                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 ChatbotManager                          │
│           (Orchestrates interview flow)                 │
└─┬───────────────┬───────────────┬───────────────────┬───┘
  │               │               │                   │
  ▼               ▼               ▼                   ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐ ┌─────────────┐
│   LLM    │ │Validation│ │  Question    │ │  Storage    │
│ Service  │ │ Service  │ │  Generator   │ │  Service    │
└──────────┘ └──────────┘ └──────────────┘ └─────────────┘
     │                           │                  │
     ▼                           ▼                  ▼
┌──────────┐              ┌──────────┐       ┌──────────┐
│Groq API  │              │System    │       │  JSON    │
│(Llama)   │              │Prompts   │       │  Files   │
└──────────┘              └──────────┘       └──────────┘
```

---

## 💡 How It Works

### Interview Flow:
```
START → Greeting
   ↓
1. Info Gathering (Name, Email, Phone, Experience, Position, Location)
   ↓
2. Tech Stack Declaration (e.g., "Python, React, Docker, AWS")
   ↓
3. Technical Questions (3 questions per technology)
   │  - Difficulty adapts to role
   │  - User can skip with "I don't know"
   ↓
4. Closing (Thank you + Next steps)
   ↓
END → Data saved to JSON
```

### Question Difficulty Adaptation:

**Junior Developer** (0-2 years)
- Fundamentals and syntax
- "What are Python decorators?"
- "Explain the difference between let and var in JavaScript"

**Mid-Level Developer** (2-5 years)
- Practical application and debugging
- "How would you optimize a slow database query?"
- "Describe a time you debugged a production issue"

**Senior Developer** (5-10 years)
- Architecture and design patterns
- "Design a caching strategy for a high-traffic API"
- "Explain trade-offs between microservices and monolithic architecture"

**Architect** (10+ years)
- System design and scalability
- "Design a distributed system handling 1M concurrent users"
- "How would you migrate a legacy system to the cloud?"

---

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "GROQ_API_KEY=your_key_here" > .env

# Run application
streamlit run app.py
```

### Get Groq API Key (Free)

1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up with GitHub/Google
3. Navigate to "API Keys"
4. Create new key
5. Copy to `.env` file

---

## 📂 Project Structure
```
talentscout-hiring-assistant/
│
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
│
├── src/
│   ├── chatbot/
│   │   ├── manager.py             # Interview orchestration
│   │   └── conversation_flow.py   # Stage management
│   │
│   ├── services/
│   │   ├── llm_service.py         # Groq API integration
│   │   ├── question_generator.py  # Dynamic question generation
│   │   ├── validation_service.py  # Input validation
│   │   ├── storage_service.py     # JSON data persistence
│   │   └── sentiment_service.py   # Answer quality analysis
│   │
│   └── utils/
│       ├── constants.py           # Constants & enums
│       └── helpers.py             # Utility functions
│
└── data/
    └── candidates/                # Interview JSON files
```

---

## 🎨 Features

### ✅ Core Features
- Real-time chat interface (like ChatGPT/Claude)
- Role-based question difficulty adaptation
- "I don't know" handling (skip questions gracefully)
- Answer quality validation (length, relevance, sentiment)
- Exit anytime with "exit", "quit", "bye"
- Auto-save after each answer
- Unique candidate IDs with timestamps
- Multi-technology support (up to 5 technologies)

### 🔮 Future Enhancements
- Video recording for facial sentiment analysis
- Question time limits (2 min per question)
- Tab-switching detection (anti-cheating)
- Copy-paste prevention
- Real-time admin dashboard
- Multi-language support (Spanish, French, Hindi)
- Email notifications to recruiters
- ATS system integration

---

## 📊 Sample Output

Candidate data is saved as JSON in `data/candidates/`:
```json
{
  "candidate_id": "CAND_20241231120000_a1b2c3d4",
  "name": "John Doe",
  "email": "john@example.com",
  "experience": 5.0,
  "position": "Senior Developer",
  "tech_stack": ["python", "react", "docker"],
  "technical_qa": {
    "python": [
      {
        "question": "How would you optimize performance in a Python application?",
        "answer": "I would use caching, database indexing, and async processing...",
        "skipped": false,
        "metrics": {
          "sentiment": 0.75,
          "length": 250,
          "relevance": 0.85
        }
      }
    ]
  },
  "final_metrics": {
    "total_questions": 9,
    "questions_answered": 8,
    "questions_skipped": 1,
    "avg_sentiment": 0.72,
    "completion_rate": 100.0
  }
}
```

---

## 🔧 Tech Stack Details

### Frontend
- **Streamlit 1.29.0** - Python web framework with built-in chat components
- **Custom CSS** - Gradient backgrounds, message bubbles, responsive design

### Backend
- **Python 3.9+** - Core application logic
- **Groq API** - LLM inference with Llama 3.3 70B
- **TextBlob** - Sentiment analysis and NLP
- **JSON** - Data persistence

### Key Libraries
```python
streamlit==1.29.0        # Web framework
requests==2.31.0         # HTTP client for Groq API
textblob==0.17.1         # Sentiment analysis
python-dotenv==1.0.0     # Environment variables
langdetect==1.0.9        # Language detection
```

---

## 🤝 Contributing

This project was built as part of an AI/ML internship assignment. Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📄 License

MIT License - Free to use for personal or commercial projects.

---

## 👨‍💻 Author

**GeorgeJiss**

Built with ❤️ using Streamlit, Groq, and Llama 3.3

---

## 🙏 Acknowledgments

- **Groq** - Ultra-fast LLM inference platform
- **Meta AI** - Llama 3.3 70B language model
- **Streamlit** - Rapid web app development
- **TextBlob** - Simple NLP and sentiment analysis

---

**⭐ Star this repo if you found it useful!**
