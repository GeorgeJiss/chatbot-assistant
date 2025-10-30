from typing import Optional, Dict, Any
from src.utils.constants import ConversationStage, InfoField, INFO_PROMPTS
from src.services.validation_service import ValidationService

class ConversationFlow:
    """Manages the flow of conversation through different stages"""
    
    def __init__(self):
        self.validator = ValidationService()
        
        # Define the order of information collection
        self.info_collection_order = [
            InfoField.NAME,
            InfoField.EMAIL,
            InfoField.PHONE,
            InfoField.EXPERIENCE,
            InfoField.POSITION,
            InfoField.LOCATION,
        ]
        
        self.current_info_index = 0
    
    def get_current_stage(self, candidate_data: Dict[str, Any]) -> ConversationStage:
        """
        Determine current conversation stage based on collected data
        
        Args:
            candidate_data: Dictionary of collected candidate information
            
        Returns:
            Current conversation stage
        """
        # Check if all basic info is collected
        basic_fields = [
            'name', 'email', 'phone', 'experience', 'position', 'location'
        ]
        
        basic_info_complete = all(
            field in candidate_data and candidate_data[field]
            for field in basic_fields
        )
        
        if not basic_info_complete:
            return ConversationStage.INFO_GATHERING
        
        # Check if tech stack is declared
        if 'tech_stack' not in candidate_data or not candidate_data['tech_stack']:
            return ConversationStage.TECH_STACK
        
        # Check if technical questions are in progress
        if 'technical_qa' in candidate_data and candidate_data.get('qa_in_progress', False):
            return ConversationStage.TECHNICAL_QUESTIONS
        
        # Check if all technical questions are answered
        if 'technical_qa' in candidate_data:
            tech_stack = candidate_data.get('tech_stack', [])
            qa = candidate_data.get('technical_qa', {})
            
            # Check if we have enough answers
            total_expected = len(tech_stack) * 3  # 3 questions per tech
            total_answered = sum(len(answers) for answers in qa.values())
            
            if total_answered < total_expected:
                return ConversationStage.TECHNICAL_QUESTIONS
        
        # Check if tech stack exists but no QA started
        if 'tech_stack' in candidate_data and 'technical_qa' not in candidate_data:
            return ConversationStage.TECHNICAL_QUESTIONS
        
        # All done
        return ConversationStage.CLOSING
    
    def get_next_info_field(self, candidate_data: Dict[str, Any]) -> Optional[InfoField]:
        """
        Get the next information field to collect
        
        Args:
            candidate_data: Dictionary of collected candidate information
            
        Returns:
            Next InfoField to collect or None if all collected
        """
        for field in self.info_collection_order:
            field_name = field.value
            
            if field_name not in candidate_data or not candidate_data[field_name]:
                return field
        
        return None
    
    def get_next_prompt(self, candidate_data: Dict[str, Any]) -> str:
        """
        Get the next prompt to show to user
        
        Args:
            candidate_data: Dictionary of collected candidate information
            
        Returns:
            Prompt string
        """
        stage = self.get_current_stage(candidate_data)
        
        if stage == ConversationStage.INFO_GATHERING:
            next_field = self.get_next_info_field(candidate_data)
            if next_field:
                return INFO_PROMPTS.get(next_field, "Please provide the requested information.")
        
        elif stage == ConversationStage.TECH_STACK:
            return INFO_PROMPTS.get(InfoField.TECH_STACK, "Please list your tech stack.")
        
        return ""
    
    def validate_response(
        self,
        field: InfoField,
        response: str
    ) -> tuple:
        """
        Validate user response for a specific field
        
        Args:
            field: Information field
            response: User's response
            
        Returns:
            Tuple of (is_valid, error_message, parsed_value)
        """
        if field == InfoField.NAME:
            is_valid, error = self.validator.validate_name(response)
            return is_valid, error, response.strip() if is_valid else None
        
        elif field == InfoField.EMAIL:
            is_valid, error = self.validator.validate_email(response)
            return is_valid, error, response.strip().lower() if is_valid else None
        
        elif field == InfoField.PHONE:
            is_valid, error = self.validator.validate_phone(response)
            return is_valid, error, response.strip() if is_valid else None
        
        elif field == InfoField.EXPERIENCE:
            is_valid, error, years = self.validator.validate_experience(response)
            return is_valid, error, years
        
        elif field == InfoField.POSITION:
            is_valid, error = self.validator.validate_position(response)
            return is_valid, error, response.strip() if is_valid else None
        
        elif field == InfoField.LOCATION:
            is_valid, error = self.validator.validate_location(response)
            return is_valid, error, response.strip() if is_valid else None
        
        elif field == InfoField.TECH_STACK:
            is_valid, error, techs = self.validator.validate_tech_stack(response)
            return is_valid, error, techs
        
        return False, "Unknown field type", None
    
    def should_transition_stage(
        self,
        current_stage: ConversationStage,
        candidate_data: Dict[str, Any]
    ) -> bool:
        """
        Check if should transition to next stage
        
        Args:
            current_stage: Current conversation stage
            candidate_data: Collected candidate data
            
        Returns:
            True if should transition, False otherwise
        """
        actual_stage = self.get_current_stage(candidate_data)
        return actual_stage != current_stage
    
    def get_progress_summary(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of conversation progress
        
        Args:
            candidate_data: Collected candidate data
            
        Returns:
            Dictionary with progress information
        """
        basic_fields = ['name', 'email', 'phone', 'experience', 'position', 'location']
        collected_basic = sum(
            1 for field in basic_fields
            if field in candidate_data and candidate_data[field]
        )
        
        tech_stack_collected = 'tech_stack' in candidate_data and candidate_data['tech_stack']
        
        questions_answered = 0
        total_questions = 0
        
        if 'tech_stack' in candidate_data and candidate_data['tech_stack']:
            total_questions = len(candidate_data['tech_stack']) * 3
            
            if 'technical_qa' in candidate_data:
                questions_answered = sum(
                    len(answers)
                    for answers in candidate_data['technical_qa'].values()
                )
        
        return {
            'basic_info_collected': collected_basic,
            'basic_info_total': len(basic_fields),
            'tech_stack_collected': tech_stack_collected,
            'questions_answered': questions_answered,
            'total_questions': total_questions,
            'current_stage': self.get_current_stage(candidate_data).value
        }
    
    def is_complete(self, candidate_data: Dict[str, Any]) -> bool:
        """
        Check if conversation is complete
        
        Args:
            candidate_data: Collected candidate data
            
        Returns:
            True if complete, False otherwise
        """
        stage = self.get_current_stage(candidate_data)
        return stage == ConversationStage.CLOSING