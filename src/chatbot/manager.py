"""
Main chatbot manager - orchestrates the conversation (NO VOICE)
Enhanced with "I don't know" handling and rollback
"""

from typing import Optional, Dict, Any
import random
from datetime import datetime

from src.utils.constants import (
    ConversationStage, InfoField, GREETING_MESSAGE, 
    CLOSING_MESSAGE, EXIT_KEYWORDS, FALLBACK_RESPONSES
)
from src.chatbot.conversation_flow import ConversationFlow
from src.services.llm_service import LLMService
from src.services.storage_service import StorageService
from src.services.sentiment_service import SentimentService
from src.prompts.question_generator import QuestionGenerator
from src.utils.helpers import generate_session_id
import config

# Keywords indicating "I don't know"
DONT_KNOW_KEYWORDS = [
    "don't know", "dont know", "do not know",
    "not sure", "unsure", "no idea", "not aware",
    "don't understand", "dont understand",
    "never used", "not familiar", "no experience",
    "i am not aware", "not aware"
]

class ChatbotManager:
    """Main chatbot manager - TEXT ONLY, ROLE-BASED QUESTIONS"""
    
    def __init__(self):
        self.session_id = generate_session_id()
        self.current_stage = ConversationStage.GREETING
        
        # Initialize services (NO VOICE)
        self.llm_service = LLMService()
        self.storage_service = StorageService()
        self.conversation_flow = ConversationFlow()
        self.question_generator = QuestionGenerator()
        self.sentiment_service = SentimentService()
        
        # Candidate data storage
        self.candidate_data = {}
        self.candidate_id = None
        
        # Technical Q&A tracking
        self.current_tech = None
        self.current_question = None
        self.question_count = 0
        self.total_questions = 0
        
        # Track skipped questions
        self.skipped_questions = []
        
        # Conversation history
        self.conversation_history = []
        
        # Metrics
        self.metrics = {
            'sentiment_scores': [],
            'answer_lengths': [],
            'relevance_scores': [],
            'questions_skipped': 0
        }
        
        print(f"✅ ChatbotManager initialized - Session: {self.session_id}")
    
    def get_greeting(self) -> str:
        """Get initial greeting message"""
        self.current_stage = ConversationStage.INFO_GATHERING
        return GREETING_MESSAGE
    
    def process_message(self, user_message: str) -> Dict[str, Any]:
        """Process user message and generate response"""
        print(f"\n{'='*60}")
        print(f"Processing: '{user_message[:50]}...'")
        print(f"Stage: {self.current_stage}")
        
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Determine stage
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
            response_data = {'response': self._get_fallback_response()}
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response_data['response'],
            "timestamp": datetime.now().isoformat()
        })
        
        # Save after every interaction
        self._save_candidate_data()
        
        print(f"Response generated")
        print(f"{'='*60}\n")
        
        return response_data
    
    def _handle_info_gathering(self, user_message: str) -> Dict[str, Any]:
        """Handle information gathering stage"""
        next_field = self.conversation_flow.get_next_info_field(self.candidate_data)
        
        if not next_field:
            self.current_stage = ConversationStage.TECH_STACK
            return self._handle_tech_stack("")
        
        # Validate response
        is_valid, error, parsed_value = self.conversation_flow.validate_response(
            next_field,
            user_message
        )
        
        if is_valid:
            self.candidate_data[next_field.value] = parsed_value
            print(f"✅ Stored {next_field.value}: {parsed_value}")
            
            # Get next field
            next_field_after = self.conversation_flow.get_next_info_field(self.candidate_data)
            
            if next_field_after:
                acknowledgment = self._generate_acknowledgment(next_field)
                next_prompt = self.conversation_flow.get_next_prompt(self.candidate_data)
                return {'response': f"{acknowledgment}\n\n{next_prompt}"}
            else:
                acknowledgment = "Perfect! I have all your basic information."
                tech_prompt = self.conversation_flow.get_next_prompt(self.candidate_data)
                return {'response': f"{acknowledgment}\n\n{tech_prompt}"}
        else:
            return {'response': f"{error}\n\n{self.conversation_flow.get_next_prompt(self.candidate_data)}"}
    
    def _handle_tech_stack(self, user_message: str) -> Dict[str, Any]:
        """Handle tech stack declaration"""
        if not user_message or user_message.strip() == "":
            return {'response': self.conversation_flow.get_next_prompt(self.candidate_data)}
        
        is_valid, error, tech_list = self.conversation_flow.validate_response(
            InfoField.TECH_STACK,
            user_message
        )
        
        if is_valid:
            tech_list = tech_list[:config.MAX_TECH_STACK_ITEMS]
            
            self.candidate_data['tech_stack'] = tech_list
            self.candidate_data['technical_qa'] = {}
            self.candidate_data['qa_in_progress'] = True
            
            self.total_questions = len(tech_list) * config.QUESTIONS_PER_TECH
            self.question_count = 0
            
            print(f"✅ Tech stack: {tech_list}")
            print(f"📊 Total questions: {self.total_questions}")
            
            self.current_stage = ConversationStage.TECHNICAL_QUESTIONS
            
            role = self.candidate_data.get('position', '')
            experience = self.candidate_data.get('experience', 0)
            tech_display = ', '.join([t.title() for t in tech_list])
            
            intro = f"""Excellent! I see you're proficient in: **{tech_display}**.

Based on your role as **{role}** with **{experience} years** of experience, I'll now ask you **{self.total_questions} technical questions** tailored to your level.

Let's begin!"""
            
            first_question = self._get_next_technical_question()
            
            if first_question:
                return {'response': f"{intro}\n\n{first_question}"}
            else:
                return {'response': "I'm sorry, I couldn't generate questions."}
        else:
            return {'response': f"{error}\n\nPlease list 1-{config.MAX_TECH_STACK_ITEMS} technologies separated by commas."}
    
    def _handle_technical_questions(self, user_message: str) -> Dict[str, Any]:
        """Handle technical questions with 'I don't know' support"""
        
        if self.current_question and user_message.strip():
            print(f"📝 Processing answer for: {self.current_tech}")
            
            # Check if user doesn't know the answer
            if self._is_dont_know_answer(user_message):
                return self._handle_dont_know_answer()
            
            # Validate answer quality
            is_valid, feedback, metrics = self.sentiment_service.validate_answer_quality(
                user_message,
                self.current_question
            )
            
            if not is_valid:
                print(f"⚠️ Invalid answer: {feedback}")
                return {'response': f"{feedback}\n\nIf you don't know the answer, you can type \"I don't know\" and we'll move to the next question."}
            
            # Calculate relevance
            relevance = self.sentiment_service.check_answer_relevance(
                user_message,
                self.current_question,
                self.current_tech
            )
            
            # Store metrics
            self.metrics['sentiment_scores'].append(metrics['sentiment']['polarity'])
            self.metrics['answer_lengths'].append(metrics['length'])
            self.metrics['relevance_scores'].append(relevance)
            
            # Store answer
            if self.current_tech not in self.candidate_data['technical_qa']:
                self.candidate_data['technical_qa'][self.current_tech] = []
            
            self.candidate_data['technical_qa'][self.current_tech].append({
                'question': self.current_question,
                'answer': user_message.strip(),
                'timestamp': datetime.now().isoformat(),
                'skipped': False,
                'metrics': {
                    'sentiment': metrics['sentiment']['polarity'],
                    'length': metrics['length'],
                    'relevance': relevance
                }
            })
            
            self.question_count += 1
            print(f"✅ Progress: {self.question_count}/{self.total_questions}")
            
            # Clear current question
            self.current_question = None
            self.current_tech = None
            
            # Get next question
            next_question = self._get_next_technical_question()
            
            if next_question:
                acknowledgments = [
                    "Thank you for your answer.",
                    "Got it, thanks!",
                    "Great, let's continue.",
                    "Thanks! Next question:"
                ]
                acknowledgment = random.choice(acknowledgments)
                return {'response': f"{acknowledgment}\n\n{next_question}"}
            else:
                # All done
                print("✅ All questions completed!")
                self.candidate_data['qa_in_progress'] = False
                self.candidate_data['final_metrics'] = self._calculate_final_metrics()
                self.current_stage = ConversationStage.CLOSING
                return self._handle_closing()
        else:
            # Get next question
            next_question = self._get_next_technical_question()
            if next_question:
                return {'response': next_question}
            else:
                self.current_stage = ConversationStage.CLOSING
                return self._handle_closing()
    
    def _is_dont_know_answer(self, answer: str) -> bool:
        """Check if answer indicates 'I don't know'"""
        answer_lower = answer.lower().strip()
        
        # Exact short answers
        if answer_lower in ["idk", "no", "nope", "skip"]:
            return True
        
        # Check for keywords
        return any(keyword in answer_lower for keyword in DONT_KNOW_KEYWORDS)
    
    def _handle_dont_know_answer(self) -> Dict[str, Any]:
        """Handle when user doesn't know the answer"""
        print(f"⚠️ User doesn't know answer for: {self.current_tech}")
        
        # Store as skipped
        if self.current_tech not in self.candidate_data['technical_qa']:
            self.candidate_data['technical_qa'][self.current_tech] = []
        
        self.candidate_data['technical_qa'][self.current_tech].append({
            'question': self.current_question,
            'answer': "Question skipped - candidate indicated they don't know",
            'timestamp': datetime.now().isoformat(),
            'skipped': True,
            'metrics': {
                'sentiment': 0,
                'length': 0,
                'relevance': 0
            }
        })
        
        self.question_count += 1
        self.metrics['questions_skipped'] += 1
        
        print(f"✅ Skipped. Progress: {self.question_count}/{self.total_questions}")
        
        # Clear current question
        self.current_question = None
        self.current_tech = None
        
        # Get next question
        next_question = self._get_next_technical_question()
        
        if next_question:
            response = f"""That's okay! It's perfectly fine to not know everything.

Let's move on to the next question.

{next_question}"""
            return {'response': response}
        else:
            # All done
            self.candidate_data['qa_in_progress'] = False
            self.candidate_data['final_metrics'] = self._calculate_final_metrics()
            self.current_stage = ConversationStage.CLOSING
            return self._handle_closing()
    
    def _get_next_technical_question(self) -> Optional[str]:
        """Get next technical question with role-based difficulty"""
        tech_stack = self.candidate_data.get('tech_stack', [])
        answered_qa = self.candidate_data.get('technical_qa', {})
        role = self.candidate_data.get('position', '')
        experience = self.candidate_data.get('experience', 0)
        
        for tech in tech_stack:
            answered_count = len(answered_qa.get(tech, []))
            
            if answered_count < config.QUESTIONS_PER_TECH:
                # Generate questions
                questions = self.question_generator.generate_questions_for_tech(
                    tech,
                    role=role,
                    experience_years=experience,
                    num_questions=config.QUESTIONS_PER_TECH
                )
                
                # Find unanswered
                for question in questions:
                    already_answered = any(
                        qa['question'] == question
                        for qa in answered_qa.get(tech, [])
                    )
                    
                    if not already_answered:
                        self.current_tech = tech
                        self.current_question = question
                        
                        return self.question_generator.format_question(
                            tech,
                            question,
                            self.question_count + 1,
                            self.total_questions
                        )
        
        return None
    
    def _handle_closing(self) -> Dict[str, Any]:
        """Handle closing"""
        self.candidate_data['qa_in_progress'] = False
        self.candidate_data['completed_at'] = datetime.now().isoformat()
        return {
            'response': CLOSING_MESSAGE,
            'end_conversation': True
        }
    
    def _calculate_final_metrics(self) -> Dict:
        """Calculate final metrics"""
        answered = self.question_count - self.metrics['questions_skipped']
        
        metrics = {
            'total_questions': self.question_count,
            'questions_answered': answered,
            'questions_skipped': self.metrics['questions_skipped'],
            'completion_rate': (self.question_count / self.total_questions * 100) if self.total_questions > 0 else 0,
            'avg_sentiment': 0,
            'avg_answer_length': 0,
            'avg_relevance': 0
        }
        
        if self.metrics['sentiment_scores']:
            metrics['avg_sentiment'] = sum(self.metrics['sentiment_scores']) / len(self.metrics['sentiment_scores'])
        
        if self.metrics['answer_lengths']:
            metrics['avg_answer_length'] = sum(self.metrics['answer_lengths']) / len(self.metrics['answer_lengths'])
        
        if self.metrics['relevance_scores']:
            metrics['avg_relevance'] = sum(self.metrics['relevance_scores']) / len(self.metrics['relevance_scores'])
        
        return metrics
    
    def _save_candidate_data(self):
        """Save to JSON"""
        try:
            candidate_id = self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
            if candidate_id:
                self.candidate_id = candidate_id
        except Exception as e:
            print(f"❌ Save error: {e}")
    
    def _generate_acknowledgment(self, field: InfoField) -> str:
        """Generate acknowledgment"""
        acknowledgments = {
            InfoField.NAME: ["Great!", "Thank you!", "Perfect!", "Nice to meet you!"],
            InfoField.EMAIL: ["Got it!", "Recorded.", "Perfect!"],
            InfoField.PHONE: ["Thank you!", "Noted.", "Got it!"],
            InfoField.EXPERIENCE: ["Excellent!", "Great!", "Understood!"],
            InfoField.POSITION: ["Interesting!", "Great choice!", "Excellent!"],
            InfoField.LOCATION: ["Perfect!", "Got it!", "Thank you!"]
        }
        return random.choice(acknowledgments.get(field, ["Thank you!"]))
    
    def _get_fallback_response(self) -> str:
        """Fallback response"""
        return random.choice(FALLBACK_RESPONSES)
    
    def handle_exit(self) -> Dict[str, Any]:
        """Handle exit"""
        if self.candidate_data:
            self.candidate_data['incomplete'] = True
            self.candidate_data['exit_time'] = datetime.now().isoformat()
            self._save_candidate_data()
        
        return {
            'response': "Thank you for your time! Your progress has been saved. Have a great day!",
            'end_conversation': True
        }