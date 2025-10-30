"""
TalentScout AI Hiring Assistant
Main Streamlit Application
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.chatbot.manager import ChatbotManager
from src.utils.constants import ConversationStage, EXIT_KEYWORDS
import config

# Page configuration
st.set_page_config(
    page_title="TalentScout AI Hiring Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - IMPROVED VERSION
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0e1117;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Chat message containers */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        word-wrap: break-word;
        overflow-wrap: break-word;
        max-width: 100%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        margin-left: 2rem;
        border-left: 4px solid #2196F3;
        color: #1a1a1a;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
        margin-right: 2rem;
        border-left: 4px solid #667eea;
        color: #1a1a1a;
    }
    
    .message-label {
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #333;
    }
    
    .message-content {
        color: #2c3e50;
        font-size: 1rem;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
    }
    
    /* Info and success boxes */
    .info-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        color: #856404;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #b8e6c0 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        color: #155724;
    }
    
    .success-box strong {
        font-size: 1.2rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    
    .css-1d391kg p, [data-testid="stSidebar"] p {
        color: #e0e0e0;
    }
    
    /* Input field styling */
    .stChatInput {
        background-color: #2c3e50;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress indicators */
    .progress-item {
        color: #4CAF50;
        font-weight: 500;
        margin: 0.3rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotManager()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add greeting message
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
    
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False

def display_header():
    """Display application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TalentScout AI Hiring Assistant</h1>
        <p>Intelligent Candidate Screening for Technology Placements</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with information"""
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This AI assistant helps streamline the initial candidate screening process by:
        
        - 📝 Gathering essential candidate information
        - 💻 Assessing technical proficiency
        - 🎯 Generating relevant tech questions
        - ⚡ Providing instant feedback
        """)
        
        st.divider()
        
        st.header("🔐 Privacy")
        st.write("""
        Your data is:
        - Stored locally only
        - GDPR compliant
        - Not shared with third parties
        """)
        
        st.divider()
        
        st.header("💡 Tips")
        st.write("""
        - Be specific about your tech stack
        - Answer questions thoroughly
        - Type 'exit', 'quit', or 'bye' to end
        """)
        
        if st.session_state.chatbot.current_stage != ConversationStage.GREETING:
            st.divider()
            st.header("📊 Progress")
            stage_names = {
                ConversationStage.GREETING: "Greeting",
                ConversationStage.INFO_GATHERING: "Info Gathering",
                ConversationStage.TECH_STACK: "Tech Stack",
                ConversationStage.TECHNICAL_QUESTIONS: "Technical Q&A",
                ConversationStage.CLOSING: "Closing"
            }
            current = stage_names.get(st.session_state.chatbot.current_stage, "Unknown")
            st.info(f"**Current Stage:** {current}")
            
            # Show collected info
            if st.session_state.chatbot.candidate_data:
                st.write("**Collected Data:**")
                data = st.session_state.chatbot.candidate_data
                if data.get('name'):
                    st.markdown('<p class="progress-item">✓ Name</p>', unsafe_allow_html=True)
                if data.get('email'):
                    st.markdown('<p class="progress-item">✓ Email</p>', unsafe_allow_html=True)
                if data.get('phone'):
                    st.markdown('<p class="progress-item">✓ Phone</p>', unsafe_allow_html=True)
                if data.get('experience'):
                    st.markdown('<p class="progress-item">✓ Experience</p>', unsafe_allow_html=True)
                if data.get('position'):
                    st.markdown('<p class="progress-item">✓ Position</p>', unsafe_allow_html=True)
                if data.get('location'):
                    st.markdown('<p class="progress-item">✓ Location</p>', unsafe_allow_html=True)
                if data.get('tech_stack'):
                    st.markdown('<p class="progress-item">✓ Tech Stack</p>', unsafe_allow_html=True)

def display_chat_history():
    """Display chat message history"""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        # Escape HTML in content to prevent rendering issues
        import html
        safe_content = html.escape(content)
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-label">👤 You</div>
                <div class="message-content">{safe_content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-label">🤖 Assistant</div>
                <div class="message-content">{safe_content}</div>
            </div>
            """, unsafe_allow_html=True)

def check_exit_keyword(user_input: str) -> bool:
    """Check if user wants to exit"""
    return any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS)

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Display chat history
    display_chat_history()
    
    # Check if conversation has ended
    if st.session_state.conversation_ended:
        st.markdown("""
        <div class="success-box">
            <strong>✅ Conversation Ended</strong>
            <p>Thank you for using TalentScout AI! Refresh the page to start a new session.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Start New Session", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Check for exit keywords
        if check_exit_keyword(user_input):
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get closing message
            closing_msg = st.session_state.chatbot.handle_exit()
            st.session_state.messages.append({
                "role": "assistant",
                "content": closing_msg
            })
            
            st.session_state.conversation_ended = True
            st.rerun()
        else:
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get chatbot response
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.chatbot.process_message(user_input)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Check if conversation naturally ended
            if st.session_state.chatbot.current_stage == ConversationStage.CLOSING:
                if "thank you" in response.lower() or "next steps" in response.lower():
                    st.session_state.conversation_ended = True
            
            st.rerun()

if __name__ == "__main__":
    main()