import streamlit as st
import sys
from pathlib import Path
import time

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.chatbot.manager import ChatbotManager
from src.utils.constants import EXIT_KEYWORDS
import config

# Page configuration
st.set_page_config(
    page_title="TalentScout AI Hiring Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - FIXED
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: transparent;
        border-radius: 15px;
        padding: 1rem 1rem 5rem 1rem;
        margin: 1rem auto;
        max-width: 800px;
        box-shadow: none;
    }
    
    .header {
        text-align: center;
        color: #ffffff; 
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.5); 
    }
    
    .header h1 {
        margin: 0;
        font-size: 2rem;
        color: #ffffff;
    }
    
    .header p {
        margin: 0.5rem 0 0 0;
        color: #f0f0f0;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        
        border-radius: 10px;
        padding: 1rem; 
        margin: 1rem 0;
        
        max-height: 500px; 
        overflow-y: auto;
    }
    
    .message {
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        animation: fadeIn 0.3s ease-in;
        clear: both;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        text-align: left;
    }
    
    .assistant-message {
        background: #ffffff;
        color: #1a1a1a;
        margin-right: 20%;
        border: 1px solid #e0e0e0;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    

    /* --- CSS for st.chat_input --- */
    
    [data-testid="stChatInput"] {
        background: transparent !important;
    }
    
    /* This targets the actual text input field inside */
    [data-testid="stChatInput"] input {
        /* CHANGED: Made transparent to match background */
        background-color: transparent !important; 
        
        border-radius: 25px !important;
        padding: 0.75rem 1rem !important;
        
        /* CHANGED: Swapped solid border for subtle one */
        border: 1px solid rgba(255, 255, 255, 0.5) !important; 
        
        /* CHANGED: Text color to white for visibility */
        color: #ffffff !important; 
    }

    /* This targets the placeholder text (e.g., "Type your answer here...") */
    [data-testid="stChatInput"] input::placeholder {
        color: #f0f0f0 !important; /* CHANGED: Light gray placeholder */
    }

    [data-testid="stChatInput"] input:focus {
        border-color: #ffffff !important; /* CHANGED: Focus border to white */
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* This targets the send button inside */
    [data-testid="stChatInput"] button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        background: #764ba2 !important;
    }

</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotManager()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        greeting = """Hello! Welcome to TalentScout AI Hiring Assistant.

I'm here to conduct your initial screening interview for technology positions.

The interview will take approximately 10-15 minutes. I'll ask you questions about:
• Your basic information
• Your technical expertise
• Your skills through relevant questions

You can type "exit", "quit", or "bye" at any time to end the interview.

**Let's start by entering your full name.**"""
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

def display_chat_history():
    """Display chat messages"""
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(
                f'<div class="message user-message">{content}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message assistant-message">{content}</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

def process_user_input(user_input: str):
    """Process user input"""
    if not user_input or not user_input.strip():
        return
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Check for exit
    if any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS):
        response_data = st.session_state.chatbot.handle_exit()
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_data['response']
        })
        st.session_state.conversation_ended = True
        st.session_state.input_key += 1
        st.rerun() 
        return
    
    # Process message
    with st.spinner("Thinking..."):
        response_data = st.session_state.chatbot.process_message(user_input)
    
    # Add assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_data['response']
    })
    
    # Check if ended
    if response_data.get('end_conversation'):
        st.session_state.conversation_ended = True
    
    st.session_state.input_key += 1
    st.rerun()

def main():
    """Main application"""
    initialize_session_state()
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown(
        '<div class="header">'
        '<h1>🤖 TalentScout AI Hiring Assistant</h1>'
        '<p>Your AI-powered technical screening companion</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Display chat
    display_chat_history()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    if not st.session_state.conversation_ended:
        if user_input := st.chat_input("Type your answer here..."):
            process_user_input(user_input)
    else:
        st.success("✅ Interview completed! Thank you for your time.")
        
        if st.button("🔄 Start New Interview"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()