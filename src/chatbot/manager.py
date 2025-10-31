"""
Main chatbot manager - orchestrates the conversation with VOICE support
FIXED: One question at a time, proper state management, JSON storage
"""

from typing import Optional, Dict, Any
import random
import time
from datetime import datetime

from src.utils.constants import (
    ConversationStage, InfoField, GREETING_MESSAGE, 
    CLOSING_MESSAGE, EXIT_KEYWORDS, FALLBACK_RESPONSES
)
from src.chatbot.conversation_flow import ConversationFlow
from src.services.llm_service import LLMService
from src.services.storage_service import StorageService
from src.services.voice_service import VoiceService
from src.services.sentiment_service import SentimentService
from src.services.language_service import LanguageService
from src.prompts.system_prompts import get_stage_system_prompt
from src.prompts.question_generator import QuestionGenerator
from src.utils.helpers import generate_session_id
import config

class ChatbotManager:
    """Main chatbot manager with VOICE capabilities - ONE QUESTION AT A TIME"""
    
    def __init__(self):
        self.session_id = generate_session_id()
        self.current_stage = ConversationStage.GREETING
        
        # Initialize services
        self.llm_service = LLMService()
        self.storage_service = StorageService()
        self.conversation_flow = ConversationFlow()
        self.question_generator = QuestionGenerator()
        self.voice_service = VoiceService()
        self.sentiment_service = SentimentService()
        self.language_service = LanguageService()
        
        # Candidate data storage
        self.candidate_data = {}
        self.candidate_id = None
        
        # Technical Q&A tracking - ONE AT A TIME
        self.current_tech = None
        self.current_question = None
        self.question_count = 0
        self.total_questions = 0
        self.waiting_for_answer = False
        
        # Voice interaction tracking
        self.voice_enabled = config.VOICE_ENABLED
        self.current_language = 'en'
        
        # Interview timing
        self.interview_start_time = time.time()
        self.time_remaining = config.MAX_INTERVIEW_DURATION
        
        # Conversation history
        self.conversation_history = []
        
        # Metrics
        self.metrics = {
            'sentiment_scores': [],
            'answer_lengths': [],
            'relevance_scores': []
        }
        
        print(f"✅ ChatbotManager initialized - Session: {self.session_id}")
    
    def get_time_remaining(self) -> int:
        """Get remaining interview time in seconds"""
        elapsed = time.time() - self.interview_start_time
        remaining = max(0, int(self.time_remaining - elapsed))
        return remaining
    
    def is_time_exceeded(self) -> bool:
        """Check if interview time exceeded"""
        return self.get_time_remaining() == 0
    
    def get_greeting(self) -> str:
        """Get initial greeting message"""
        self.current_stage = ConversationStage.INFO_GATHERING
        greeting_text = self.language_service.get_text('greeting', self.current_language)
        return f"{greeting_text}\n\n{GREETING_MESSAGE}"
    
    def process_message(self, user_message: str, is_voice: bool = False) -> Dict[str, Any]:
        """
        Process user message and generate response - ONE QUESTION AT A TIME
        
        Args:
            user_message: User's input message
            is_voice: Whether this is from voice input
            
        Returns:
            Dictionary with response and metadata
        """
        print(f"\n{'='*60}")
        print(f"Processing message: '{user_message[:50]}...'")
        print(f"Current stage: {self.current_stage}")
        print(f"Question count: {self.question_count}/{self.total_questions}")
        
        # Check time
        if self.is_time_exceeded():
            return {
                'response': "⏰ I apologize, but we've reached the 15-minute interview limit. Thank you for your time!",
                'audio_path': None,
                'end_conversation': True
            }
        
        # Detect language if voice input
        if is_voice and user_message:
            detected_lang = self.language_service.detect_language(user_message)
            if detected_lang in config.SUPPORTED_LANGUAGES:
                self.current_language = detected_lang
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Determine current stage
        self.current_stage = self.conversation_flow.get_current_stage(self.candidate_data)
        
        # Process based on stage
        if self.current_stage == ConversationStage.INFO_GATHERING:
            response_data = self._handle_info_gathering(user_message)
        
        elif self.current_stage == ConversationStage.TECH_STACK:
            response_data = self._handle_tech_stack(user_message)
        
        elif self.current_stage == ConversationStage.TECHNICAL_QUESTIONS:
            response_data = self._handle_technical_questions(user_message)
        
        elif self.current_stage == ConversationStage.CLOSING:
            response_data = self._handle_closing()
        
        else:
            response_data = {
                'response': self._get_fallback_response(),
                'audio_path': None
            }
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_data['response'],
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate audio if voice enabled
        if self.voice_enabled and response_data.get('response'):
            audio_path = self.voice_service.text_to_speech(
                response_data['response'],
                self.current_language
            )
            response_data['audio_path'] = audio_path
        
        # Add time remaining
        response_data['time_remaining'] = self.get_time_remaining()
        
        # Save to JSON after every interaction
        self._save_candidate_data()
        
        print(f"Response generated: '{response_data['response'][:50]}...'")
        print(f"{'='*60}\n")
        
        return response_data
    
    def _handle_info_gathering(self, user_message: str) -> Dict[str, Any]:
        """Handle information gathering stage"""
        next_field = self.conversation_flow.get_next_info_field(self.candidate_data)
        
        if not next_field:
            # All info collected, move to tech stack
            self.current_stage = ConversationStage.TECH_STACK
            return self._handle_tech_stack("")
        
        # Validate the response
        is_valid, error, parsed_value = self.conversation_flow.validate_response(
            next_field,
            user_message
        )
        
        if is_valid:
            self.candidate_data[next_field.value] = parsed_value
            print(f"✅ Stored {next_field.value}: {parsed_value}")
            
            # Save immediately
            self._save_candidate_data()
            
            # Get next field
            next_field_after = self.conversation_flow.get_next_info_field(self.candidate_data)
            
            if next_field_after:
                acknowledgment = self._generate_acknowledgment(next_field)
                next_prompt = self.conversation_flow.get_next_prompt(self.candidate_data)
                return {
                    'response': f"{acknowledgment} {next_prompt}",
                    'audio_path': None
                }
            else:
                # All basic info collected
                acknowledgment = "Perfect! I have all your basic information."
                tech_prompt = self.conversation_flow.get_next_prompt(self.candidate_data)
                return {
                    'response': f"{acknowledgment}\n\n{tech_prompt}",
                    'audio_path': None
                }
        else:
            return {
                'response': f"{error}\n\n{self.conversation_flow.get_next_prompt(self.candidate_data)}",
                'audio_path': None
            }
    
    def _handle_tech_stack(self, user_message: str) -> Dict[str, Any]:
        """Handle tech stack declaration stage"""
        if not user_message or user_message.strip() == "":
            return {
                'response': self.conversation_flow.get_next_prompt(self.candidate_data),
                'audio_path': None
            }
        
        is_valid, error, tech_list = self.conversation_flow.validate_response(
            InfoField.TECH_STACK,
            user_message
        )
        
        if is_valid:
            # Limit to MAX_TECH_STACK_ITEMS for time management
            tech_list = tech_list[:config.MAX_TECH_STACK_ITEMS]
            
            self.candidate_data['tech_stack'] = tech_list
            self.candidate_data['technical_qa'] = {}
            self.candidate_data['qa_in_progress'] = True
            
            self.total_questions = len(tech_list) * config.QUESTIONS_PER_TECH
            self.question_count = 0
            
            print(f"✅ Tech stack stored: {tech_list}")
            print(f"📊 Total questions to ask: {self.total_questions}")
            
            # Save immediately
            self._save_candidate_data()
            
            self.current_stage = ConversationStage.TECHNICAL_QUESTIONS
            
            tech_display = ', '.join([t.title() for t in tech_list])
            intro = f"Excellent! I'll assess your skills in: {tech_display}.\n\nI'll ask you {self.total_questions} technical questions, one at a time.\n\nLet's begin!"
            
            # Get first question
            first_question = self._get_next_technical_question()
            
            if first_question:
                return {
                    'response': f"{intro}\n\n{first_question}",
                    'audio_path': None
                }
            else:
                return {
                    'response': "I'm sorry, I couldn't generate questions. Let's try again.",
                    'audio_path': None
                }
        else:
            return {
                'response': f"{error}\n\nPlease list 1-{config.MAX_TECH_STACK_ITEMS} technologies separated by commas.",
                'audio_path': None
            }
    
    def _handle_technical_questions(self, user_message: str) -> Dict[str, Any]:
        """Handle technical questions stage - ONE AT A TIME"""
        
        # If we have a current question and got an answer
        if self.current_question and user_message.strip():
            print(f"📝 Processing answer for: {self.current_tech}")
            
            # Validate answer quality
            is_valid, feedback, metrics = self.sentiment_service.validate_answer_quality(
                user_message,
                self.current_question
            )
            
            if not is_valid:
                print(f"⚠️ Invalid answer: {feedback}")
                return {
                    'response': f"{feedback}\n\nPlease try again.",
                    'audio_path': None,
                    'needs_retry': True
                }
            
            # Check relevance
            relevance = self.sentiment_service.check_answer_relevance(
                user_message,
                self.current_question,
                self.current_tech
            )
            
            # Store metrics
            self.metrics['sentiment_scores'].append(metrics['sentiment']['polarity'])
            self.metrics['answer_lengths'].append(metrics['length'])
            self.metrics['relevance_scores'].append(relevance)
            
            # Store the answer in JSON structure
            if self.current_tech not in self.candidate_data['technical_qa']:
                self.candidate_data['technical_qa'][self.current_tech] = []
            
            self.candidate_data['technical_qa'][self.current_tech].append({
                'question': self.current_question,
                'answer': user_message.strip(),
                'timestamp': datetime.now().isoformat(),
                'metrics': {
                    'sentiment': metrics['sentiment']['polarity'],
                    'length': metrics['length'],
                    'relevance': relevance
                }
            })
            
            self.question_count += 1
            print(f"✅ Answer stored. Progress: {self.question_count}/{self.total_questions}")
            
            # Save immediately after each answer
            self._save_candidate_data()
            
            # Clear current question
            self.current_question = None
            self.current_tech = None
            
            # Get next question
            next_question = self._get_next_technical_question()
            
            if next_question:
                # Generate brief acknowledgment
                acknowledgment = random.choice([
                    "Thank you.",
                    "Got it.",
                    "Noted.",
                    "Thanks for your answer."
                ])
                
                return {
                    'response': f"{acknowledgment}\n\n{next_question}",
                    'audio_path': None
                }
            else:
                # All questions answered
                print("✅ All questions completed!")
                self.candidate_data['qa_in_progress'] = False
                self.candidate_data['final_metrics'] = self._calculate_final_metrics()
                self._save_candidate_data()
                
                self.current_stage = ConversationStage.CLOSING
                return self._handle_closing()
        
        else:
            # No current question, get one
            print("📋 Getting next question...")
            next_question = self._get_next_technical_question()
            
            if next_question:
                return {
                    'response': next_question,
                    'audio_path': None
                }
            else:
                # No more questions
                self.current_stage = ConversationStage.CLOSING
                return self._handle_closing()
    
    def _get_next_technical_question(self) -> Optional[str]:
        """Get next technical question - ONE AT A TIME"""
        tech_stack = self.candidate_data.get('tech_stack', [])
        answered_qa = self.candidate_data.get('technical_qa', {})
        experience = self.candidate_data.get('experience', 0)
        
        print(f"🔍 Finding next question from {len(tech_stack)} technologies")
        
        for tech in tech_stack:
            answered_count = len(answered_qa.get(tech, []))
            print(f"  - {tech}: {answered_count}/{config.QUESTIONS_PER_TECH} answered")
            
            if answered_count < config.QUESTIONS_PER_TECH:
                # Generate questions for this tech
                questions = self.question_generator.generate_questions_for_tech(
                    tech,
                    experience,
                    num_questions=config.QUESTIONS_PER_TECH
                )
                
                print(f"  - Generated {len(questions)} questions for {tech}")
                
                # Find unanswered question
                for question in questions:
                    already_answered = any(
                        qa['question'] == question
                        for qa in answered_qa.get(tech, [])
                    )
                    
                    if not already_answered:
                        # Set as current question
                        self.current_tech = tech
                        self.current_question = question
                        
                        print(f"✅ Next question set: {tech}")
                        
                        return self.question_generator.format_question(
                            tech,
                            question,
                            self.question_count + 1,
                            self.total_questions
                        )
        
        print("❌ No more questions available")
        return None
    
    def _handle_closing(self) -> Dict[str, Any]:
        """Handle closing stage"""
        self.candidate_data['qa_in_progress'] = False
        self.candidate_data['completed_at'] = datetime.now().isoformat()
        self._save_candidate_data()
        
        return {
            'response': CLOSING_MESSAGE,
            'audio_path': None,
            'end_conversation': True
        }
    
    def _calculate_final_metrics(self) -> Dict:
        """Calculate final interview metrics (hidden from candidate)"""
        metrics = {
            'avg_sentiment': 0,
            'avg_answer_length': 0,
            'avg_relevance': 0,
            'total_questions': self.question_count,
            'time_taken': time.time() - self.interview_start_time,
            'completion_rate': (self.question_count / self.total_questions * 100) if self.total_questions > 0 else 0
        }
        
        if self.metrics['sentiment_scores']:
            metrics['avg_sentiment'] = sum(self.metrics['sentiment_scores']) / len(self.metrics['sentiment_scores'])
        
        if self.metrics['answer_lengths']:
            metrics['avg_answer_length'] = sum(self.metrics['answer_lengths']) / len(self.metrics['answer_lengths'])
        
        if self.metrics['relevance_scores']:
            metrics['avg_relevance'] = sum(self.metrics['relevance_scores']) / len(self.metrics['relevance_scores'])
        
        print(f"📊 Final metrics calculated: {metrics}")
        return metrics
    
    def _save_candidate_data(self):
        """Save candidate data to JSON file"""
        try:
            candidate_id = self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
            
            if candidate_id:
                self.candidate_id = candidate_id
                print(f"💾 Data saved - Candidate ID: {candidate_id}")
            else:
                print("⚠️ Failed to save candidate data")
                
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def _generate_acknowledgment(self, field: InfoField) -> str:
        """Generate acknowledgment for collected information"""
        acknowledgments = {
            InfoField.NAME: ["Great!", "Thank you!", "Perfect!"],
            InfoField.EMAIL: ["Got it!", "Recorded.", "Perfect!"],
            InfoField.PHONE: ["Thank you!", "Noted.", "Got it!"],
            InfoField.EXPERIENCE: ["Excellent!", "Thank you.", "Got it!"],
            InfoField.POSITION: ["Great!", "Interesting!", "Excellent!"],
            InfoField.LOCATION: ["Perfect!", "Got it!", "Thank you!"]
        }
        return random.choice(acknowledgments.get(field, ["Thank you!"]))
    
    def _get_fallback_response(self) -> str:
        """Get fallback response for unclear input"""
        return random.choice(FALLBACK_RESPONSES)
    
    def handle_exit(self) -> Dict[str, Any]:
        """Handle conversation exit"""
        if self.candidate_data:
            self.candidate_data['incomplete'] = True
            self.candidate_data['exit_time'] = datetime.now().isoformat()
            self._save_candidate_data()
            print(f"👋 Interview exited - Data saved")
        
        return {
            'response': "Thank you for your time! Your session has been saved. Have a great day!",
            'audio_path': None,
            'end_conversation': True
        }
    
    def get_candidate_summary(self) -> str:
        """Get summary of collected candidate data (for admin only)"""
        from src.utils.helpers import create_candidate_summary
        return create_candidate_summary(self.candidate_data)