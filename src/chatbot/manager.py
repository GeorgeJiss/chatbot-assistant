from typing import Optional, Dict, Any
import random

from src.utils.constants import (
    ConversationStage, InfoField, GREETING_MESSAGE, 
    CLOSING_MESSAGE, EXIT_MESSAGE, FALLBACK_RESPONSES
)
from src.chatbot.conversation_flow import ConversationFlow
from src.services.llm_service import LLMService
from src.services.storage_service import StorageService
from src.prompts.system_prompts import get_stage_system_prompt, get_info_field_prompt
from src.prompts.question_generator import QuestionGenerator
from src.utils.helpers import generate_session_id

class ChatbotManager:
    """Main chatbot manager coordinating all components"""
    
    def __init__(self):
        self.session_id = generate_session_id()
        self.current_stage = ConversationStage.GREETING
        
        # Initialize services
        self.llm_service = LLMService()
        self.storage_service = StorageService()
        self.conversation_flow = ConversationFlow()
        self.question_generator = QuestionGenerator()
        
        # Candidate data storage
        self.candidate_data = {}
        
        # Technical Q&A tracking
        self.current_tech = None
        self.current_question = None
        self.question_count = 0
        self.total_questions = 0
        
        # Conversation history for context
        self.conversation_history = []
    
    def get_greeting(self) -> str:
        """Get initial greeting message"""
        self.current_stage = ConversationStage.INFO_GATHERING
        return GREETING_MESSAGE
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: User's input message
            
        Returns:
            Bot's response
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Determine current stage
        self.current_stage = self.conversation_flow.get_current_stage(
            self.candidate_data
        )
        
        # Process based on stage
        if self.current_stage == ConversationStage.INFO_GATHERING:
            response = self._handle_info_gathering(user_message)
        
        elif self.current_stage == ConversationStage.TECH_STACK:
            response = self._handle_tech_stack(user_message)
        
        elif self.current_stage == ConversationStage.TECHNICAL_QUESTIONS:
            response = self._handle_technical_questions(user_message)
        
        elif self.current_stage == ConversationStage.CLOSING:
            response = self._handle_closing()
        
        else:
            response = self._get_fallback_response()
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _handle_info_gathering(self, user_message: str) -> str:
        """Handle information gathering stage"""
        # Get next field to collect
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
            # Store the value
            self.candidate_data[next_field.value] = parsed_value
            
            # Save to storage
            self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
            
            # Get next prompt
            next_field_after = self.conversation_flow.get_next_info_field(
                self.candidate_data
            )
            
            if next_field_after:
                # Continue collecting info
                acknowledgment = self._generate_acknowledgment(next_field)
                next_prompt = self.conversation_flow.get_next_prompt(
                    self.candidate_data
                )
                return f"{acknowledgment}\n\n{next_prompt}"
            else:
                # All basic info collected, move to tech stack
                acknowledgment = "Perfect! I have all your basic information."
                tech_prompt = self.conversation_flow.get_next_prompt(
                    self.candidate_data
                )
                return f"{acknowledgment}\n\n{tech_prompt}"
        else:
            # Invalid response
            return f"{error}\n\n{self.conversation_flow.get_next_prompt(self.candidate_data)}"
    
    def _handle_tech_stack(self, user_message: str) -> str:
        """Handle tech stack declaration stage"""
        if not user_message or user_message.strip() == "":
            # First time asking
            return self.conversation_flow.get_next_prompt(self.candidate_data)
        
        # Validate tech stack
        is_valid, error, tech_list = self.conversation_flow.validate_response(
            InfoField.TECH_STACK,
            user_message
        )
        
        if is_valid:
            # Store tech stack
            self.candidate_data['tech_stack'] = tech_list
            self.candidate_data['technical_qa'] = {}
            self.candidate_data['qa_in_progress'] = True
            
            # Save to storage
            self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
            
            # Calculate total questions
            self.total_questions = len(tech_list) * self.question_generator.questions_per_tech
            self.question_count = 0
            
            # Transition to technical questions
            self.current_stage = ConversationStage.TECHNICAL_QUESTIONS
            
            # Generate acknowledgment
            tech_display = ', '.join([t.title() for t in tech_list])
            intro = f"""Excellent! I see you're proficient in: **{tech_display}**

Now I'll ask you {self.total_questions} technical questions to assess your skills. Please answer each question to the best of your ability.

Let's begin!"""
            
            # Get first question
            first_question = self._get_next_technical_question()
            
            return f"{intro}\n\n{first_question}"
        else:
            # Invalid response
            return f"{error}\n\nPlease try again and list your technologies separated by commas."
    
    def _handle_technical_questions(self, user_message: str) -> str:
        """Handle technical questions stage"""
        # If we have a current question, this is an answer
        if self.current_question and user_message.strip():
            # Validate answer
            is_valid, error = self.conversation_flow.validator.validate_answer(user_message)
            
            if not is_valid:
                return f"{error}\n\nPlease provide a more detailed answer to the question:\n\n{self.current_question}"
            
            # Store the answer
            if self.current_tech not in self.candidate_data['technical_qa']:
                self.candidate_data['technical_qa'][self.current_tech] = []
            
            self.candidate_data['technical_qa'][self.current_tech].append({
                'question': self.current_question,
                'answer': user_message.strip()
            })
            
            self.question_count += 1
            
            # Save progress
            self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
            
            # Get next question
            next_question = self._get_next_technical_question()
            
            if next_question:
                acknowledgment = random.choice([
                    "Thank you for your answer.",
                    "I've recorded your response.",
                    "Got it, thanks.",
                    "Noted.",
                ])
                return f"{acknowledgment}\n\n{next_question}"
            else:
                # All questions answered
                self.candidate_data['qa_in_progress'] = False
                self.current_stage = ConversationStage.CLOSING
                return self._handle_closing()
        else:
            # Get first question
            return self._get_next_technical_question()
    
    def _get_next_technical_question(self) -> Optional[str]:
        """Get next technical question"""
        tech_stack = self.candidate_data.get('tech_stack', [])
        answered_qa = self.candidate_data.get('technical_qa', {})
        experience = self.candidate_data.get('experience', 0)
        
        # Find next tech that needs questions
        for tech in tech_stack:
            answered_count = len(answered_qa.get(tech, []))
            
            if answered_count < self.question_generator.questions_per_tech:
                # Generate questions for this tech if not done
                questions = self.question_generator.generate_questions_for_tech(
                    tech,
                    experience
                )
                
                # Get next unanswered question
                for i, question in enumerate(questions):
                    # Check if already answered
                    already_answered = any(
                        qa['question'] == question
                        for qa in answered_qa.get(tech, [])
                    )
                    
                    if not already_answered:
                        self.current_tech = tech
                        self.current_question = question
                        
                        # Format the question
                        return self.question_generator.format_question(
                            tech,
                            question,
                            self.question_count + 1,
                            self.total_questions
                        )
        
        # No more questions
        return None
    
    def _handle_closing(self) -> str:
        """Handle closing stage"""
        # Final save
        self.candidate_data['qa_in_progress'] = False
        self.storage_service.save_candidate(
            self.candidate_data,
            self.session_id
        )
        
        return CLOSING_MESSAGE
    
    def _generate_acknowledgment(self, field: InfoField) -> str:
        """Generate acknowledgment for collected information"""
        acknowledgments = {
            InfoField.NAME: [
                "Great! Nice to meet you.",
                "Thank you!",
                "Perfect, thanks!",
            ],
            InfoField.EMAIL: [
                "Got it!",
                "Email recorded.",
                "Perfect!",
            ],
            InfoField.PHONE: [
                "Thank you!",
                "Phone number saved.",
                "Got it!",
            ],
            InfoField.EXPERIENCE: [
                "Excellent!",
                "Thank you for that information.",
                "Got it!",
            ],
            InfoField.POSITION: [
                "That's great!",
                "Interesting position!",
                "Excellent!",
            ],
            InfoField.LOCATION: [
                "Perfect!",
                "Got it!",
                "Thank you!",
            ]
        }
        
        return random.choice(acknowledgments.get(field, ["Thank you!"]))
    
    def _get_fallback_response(self) -> str:
        """Get fallback response for unclear input"""
        return random.choice(FALLBACK_RESPONSES)
    
    def handle_exit(self) -> str:
        """Handle conversation exit"""
        # Save any pending data
        if self.candidate_data:
            self.candidate_data['incomplete'] = True
            self.storage_service.save_candidate(
                self.candidate_data,
                self.session_id
            )
        
        return EXIT_MESSAGE
    
    def get_candidate_summary(self) -> str:
        """Get summary of collected candidate data"""
        from src.utils.helpers import create_candidate_summary
        return create_candidate_summary(self.candidate_data)