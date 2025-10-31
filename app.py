import streamlit as st
import sys
from pathlib import Path
import time
import html
from base64 import b64encode

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.chatbot.manager import ChatbotManager
from src.utils.constants import EXIT_KEYWORDS, ConversationStage
from src.services.voice_service import VoiceService
import config

# Page configuration
st.set_page_config(
    page_title="TalentScout AI Voice Interviewer",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS with fixed styling
st.markdown("""
<style>
    /* Main container background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Timer container - fixed positioning */
    .timer-container {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background: rgba(255, 255, 255, 0.95);
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .timer-display {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e3c72;
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    
    .timer-warning {
        color: #ff6b6b !important;
        animation: pulse-red 1s ease-in-out infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .timer-label {
        font-size: 0.7rem;
        color: #666;
        text-align: center;
        margin-top: 0.25rem;
    }
    
    /* Interview container with proper text color */
    .interview-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 2.5rem;
        margin-top: 100px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        color: #333333;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Question box with dark text */
    .question-box {
        background: #f8f9fa;
        color: #1a1a1a !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        font-size: 1.1rem;
        line-height: 1.6;
        border-left: 5px solid #667eea;
    }
    
    .question-box h2 {
        color: #1e3c72 !important;
        margin-bottom: 1rem;
    }
    
    .question-box p {
        color: #333333 !important;
    }
    
    .question-number {
        font-size: 0.9rem;
        color: #555 !important;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .question-tech {
        font-size: 0.85rem;
        opacity: 0.85;
        font-weight: 600;
        color: #1e3c72 !important;
        margin-bottom: 0.5rem;
    }
    
    /* Voice control panel */
    .voice-control-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        margin: 0.5rem;
        color: white !important;
    }
    
    .status-listening {
        background: #4CAF50;
        color: white !important;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    .status-ready {
        background: #2196F3;
        color: white !important;
    }
    
    .status-processing {
        background: #FF9800;
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:disabled {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: white !important;
        color: #333333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #333333 !important;
    }
    
    .chat-message.user {
        background: #e3f2fd;
        margin-left: 2rem;
        text-align: right;
    }
    
    .chat-message.assistant {
        background: #f5f5f5;
        margin-right: 2rem;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    /* Ensure text is visible everywhere */
    * {
        color: #333333;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e3c72 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotManager()
    if 'voice_service' not in st.session_state:
        st.session_state.voice_service = VoiceService()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
    if 'conversation_ended' not in st.session_state:
        st.session_state.conversation_ended = False
    if 'voice_mode' not in st.session_state:
        st.session_state.voice_mode = True
    if 'current_status' not in st.session_state:
        st.session_state.current_status = "ready"
    if 'current_question_formatted' not in st.session_state:
        st.session_state.current_question_formatted = None
    if 'waiting_for_answer' not in st.session_state:
        st.session_state.waiting_for_answer = True
    if 'show_chat_history' not in st.session_state:
        st.session_state.show_chat_history = False

def display_live_timer():
    """Display live countdown timer"""
    # Get time remaining from chatbot
    time_remaining = st.session_state.chatbot.get_time_remaining()
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    is_warning = time_remaining < config.WARNING_TIME
    
    timer_class = "timer-warning" if is_warning else ""
    
    # Create timer HTML
    timer_html = f"""
    <div class="timer-container">
        <div class="timer-display {timer_class}">{minutes:02d}:{seconds:02d}</div>
        <div class="timer-label">Time Remaining</div>
    </div>
    """
    
    # Display timer
    st.markdown(timer_html, unsafe_allow_html=True)
    
    # Auto-refresh every second
    if time_remaining > 0 and not st.session_state.conversation_ended:
        time.sleep(1)
        st.rerun()

def display_interview_slide():
    """Display current interview slide"""
    last_message = st.session_state.messages[-1]['content'] if st.session_state.messages else "Interview starting..."
    
    # Format current question if available
    if st.session_state.chatbot.current_question and st.session_state.chatbot.current_stage == ConversationStage.TECHNICAL_QUESTIONS:
        st.session_state.current_question_formatted = st.session_state.chatbot.question_generator.format_question(
            st.session_state.chatbot.current_tech,
            st.session_state.chatbot.current_question,
            st.session_state.chatbot.question_count + 1,
            st.session_state.chatbot.total_questions
        )
    
    # Display the question or message
    if st.session_state.current_question_formatted and st.session_state.chatbot.current_stage == ConversationStage.TECHNICAL_QUESTIONS:
        formatted_content = html.escape(st.session_state.current_question_formatted).replace("\n", "<br>")
        st.markdown(
            f'<div class="question-box"><div>{formatted_content}</div></div>',
            unsafe_allow_html=True
        )
    else:
        formatted_content = html.escape(last_message).replace("\n", "<br>")
        st.markdown(
            f'<div class="question-box"><div>{formatted_content}</div></div>',
            unsafe_allow_html=True
        )
    
    # Display controls
    display_controls()

def display_controls():
    """Display voice/text input controls"""
    st.markdown('<div class="voice-control-panel">', unsafe_allow_html=True)
    
    # Status indicator
    status_map = {
        "ready": ("Ready to Record", "status-ready"),
        "listening": ("🎤 Listening... Speak now!", "status-listening"),
        "processing": ("Processing your answer...", "status-processing")
    }
    status_text, status_class = status_map.get(st.session_state.current_status, ("Ready", "status-ready"))
    st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎤 Record Answer", key="record_btn", use_container_width=True, 
                     disabled=(st.session_state.current_status == "listening" or not st.session_state.waiting_for_answer)):
            st.session_state.current_status = "listening"
            st.rerun()
    
    with col2:
        mode_label = "💬 Switch to Text" if st.session_state.voice_mode else "🎤 Switch to Voice"
        if st.button(mode_label, key="mode_btn", use_container_width=True):
            st.session_state.voice_mode = not st.session_state.voice_mode
            st.rerun()
    
    with col3:
        if st.button("💬 Chat History", key="chat_btn", use_container_width=True):
            st.session_state.show_chat_history = not st.session_state.show_chat_history
            st.rerun()
    
    # Handle voice recording
    if st.session_state.current_status == "listening":
        with st.spinner("🎤 Listening... Speak clearly into your microphone..."):
            success, text, error = st.session_state.voice_service.speech_to_text()
        
        st.session_state.current_status = "processing"
        
        if success and text:
            process_user_input(text, is_voice=True)
        else:
            st.error(f"❌ {error or 'Could not capture audio. Please try again.'}")
            st.session_state.current_status = "ready"
            time.sleep(2)
            st.rerun()
    
    # Text input mode
    if not st.session_state.voice_mode:
        st.markdown("---")
        user_text = st.text_input(
            "Type your answer:", 
            key="text_input", 
            placeholder="Type your answer here and press Submit...",
            disabled=not st.session_state.waiting_for_answer
        )
        
        if st.button("📤 Submit Answer", key="submit_btn", use_container_width=True, 
                     disabled=not st.session_state.waiting_for_answer):
            if user_text and user_text.strip():
                st.session_state.current_status = "processing"
                process_user_input(user_text, is_voice=False)
            else:
                st.warning("⚠️ Please enter an answer before submitting.")
    
    # Show chat history if enabled
    if st.session_state.show_chat_history:
        st.markdown("---")
        st.markdown("### 💬 Conversation History")
        for msg in st.session_state.messages[-5:]:  # Show last 5 messages
            role_class = "user" if msg["role"] == "user" else "assistant"
            role_emoji = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(
                f'<div class="chat-message {role_class}">{role_emoji} {html.escape(msg["content"])}</div>',
                unsafe_allow_html=True
            )

def display_closing_slide():
    """Display closing slide"""
    last_message = st.session_state.messages[-1]['content']
    
    st.markdown(
        f"""<div class="question-box">
        <h2>✅ Interview Completed!</h2>
        <p>{html.escape(last_message).replace(chr(10), '<br>')}</p>
        </div>""",
        unsafe_allow_html=True
    )
    
    if st.button("🔄 Start New Interview", key="new_btn", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def process_user_input(user_input: str, is_voice: bool):
    """Process user input and generate response"""
    # Mark that we're not waiting for answer anymore
    st.session_state.waiting_for_answer = False
    st.session_state.current_question_formatted = None
    
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Check for exit keywords
    if any(keyword in user_input.lower() for keyword in EXIT_KEYWORDS):
        response_data = st.session_state.chatbot.handle_exit()
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_data['response']
        })
        st.session_state.conversation_ended = True
        st.session_state.current_status = "ready"
        st.rerun()
        return
    
    # Process message with chatbot
    with st.spinner("🤔 AI is thinking..."):
        response_data = st.session_state.chatbot.process_message(user_input, is_voice=is_voice)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_data['response']
    })
    
    # Play audio if available and voice mode is on
    if response_data.get('audio_path') and st.session_state.voice_mode:
        try:
            with open(response_data['audio_path'], "rb") as audio_file:
                audio_bytes = audio_file.read()
            audio_base64 = b64encode(audio_bytes).decode()
            audio_html = f"""
            <audio autoplay style='display:none;'>
                <source src='data:audio/mp3;base64,{audio_base64}' type='audio/mp3'>
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    # Check if conversation ended
    if response_data.get('end_conversation'):
        st.session_state.conversation_ended = True
    
    # Reset status and allow next answer
    st.session_state.current_status = "ready"
    st.session_state.waiting_for_answer = True
    
    # Rerun to show next question
    time.sleep(1)
    st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Check if time exceeded
    if st.session_state.chatbot.is_time_exceeded() and not st.session_state.conversation_ended:
        st.session_state.conversation_ended = True
        st.session_state.messages.append({
            "role": "assistant",
            "content": "⏰ Time's up! Thank you for participating. We will save your progress and our team will be in touch."
        })
        st.session_state.chatbot.handle_exit()
    
    # Display timer (with auto-refresh)
    display_live_timer()
    
    # Main content container
    st.markdown('<div class="interview-container">', unsafe_allow_html=True)
    
    if st.session_state.conversation_ended:
        display_closing_slide()
    else:
        display_interview_slide()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
