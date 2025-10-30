"""
Validation Service for candidate information
"""

import re
from typing import Tuple, Optional
import config

class ValidationService:
    """Service for validating user inputs"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email address
        
        Args:
            email: Email string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "Email cannot be empty"
        
        email = email.strip()
        
        if not re.match(config.EMAIL_PATTERN, email):
            return False, "Please provide a valid email address (e.g., name@example.com)"
        
        return True, None
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
        """
        Validate phone number
        
        Args:
            phone: Phone string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone or not phone.strip():
            return False, "Phone number cannot be empty"
        
        phone = phone.strip()
        
        if not re.match(config.PHONE_PATTERN, phone):
            return False, "Please provide a valid phone number"
        
        if len(re.sub(r'\D', '', phone)) < 10:
            return False, "Phone number must have at least 10 digits"
        
        return True, None
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate full name
        
        Args:
            name: Name string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Name cannot be empty"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name) > 100:
            return False, "Name is too long (max 100 characters)"
        
        # Check if name contains at least some letters
        if not re.search(r'[a-zA-Z]', name):
            return False, "Name must contain letters"
        
        return True, None
    
    @staticmethod
    def validate_experience(experience: str) -> Tuple[bool, Optional[str], Optional[float]]:
        """
        Validate years of experience
        
        Args:
            experience: Experience string to validate
            
        Returns:
            Tuple of (is_valid, error_message, parsed_years)
        """
        if not experience or not experience.strip():
            return False, "Experience cannot be empty", None
        
        # Try to extract number
        from src.utils.helpers import extract_number
        years = extract_number(experience)
        
        if years < 0:
            return False, "Experience cannot be negative", None
        
        if years > 50:
            return False, "Please provide realistic years of experience (0-50)", None
        
        return True, None, years
    
    @staticmethod
    def validate_position(position: str) -> Tuple[bool, Optional[str]]:
        """
        Validate desired position
        
        Args:
            position: Position string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not position or not position.strip():
            return False, "Position cannot be empty"
        
        position = position.strip()
        
        if len(position) < 2:
            return False, "Position must be at least 2 characters long"
        
        if len(position) > 200:
            return False, "Position description is too long (max 200 characters)"
        
        return True, None
    
    @staticmethod
    def validate_location(location: str) -> Tuple[bool, Optional[str]]:
        """
        Validate location
        
        Args:
            location: Location string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not location or not location.strip():
            return False, "Location cannot be empty"
        
        location = location.strip()
        
        if len(location) < 2:
            return False, "Location must be at least 2 characters long"
        
        if len(location) > 100:
            return False, "Location is too long (max 100 characters)"
        
        return True, None
    
    @staticmethod
    def validate_tech_stack(tech_stack: str) -> Tuple[bool, Optional[str], Optional[list]]:
        """
        Validate tech stack
        
        Args:
            tech_stack: Tech stack string to validate
            
        Returns:
            Tuple of (is_valid, error_message, parsed_list)
        """
        if not tech_stack or not tech_stack.strip():
            return False, "Tech stack cannot be empty", None
        
        from src.utils.helpers import parse_tech_stack
        techs = parse_tech_stack(tech_stack)
        
        if len(techs) < config.MIN_TECH_STACK_ITEMS:
            return False, f"Please provide at least {config.MIN_TECH_STACK_ITEMS} technology", None
        
        if len(techs) > config.MAX_TECH_STACK_ITEMS:
            return False, f"Please provide at most {config.MAX_TECH_STACK_ITEMS} technologies", None
        
        # Check each tech is valid
        for tech in techs:
            if len(tech) < 2:
                return False, f"'{tech}' is too short to be a valid technology name", None
            
            if len(tech) > 50:
                return False, f"'{tech}' is too long for a technology name", None
        
        return True, None, techs
    
    @staticmethod
    def validate_answer(answer: str, min_length: int = 10) -> Tuple[bool, Optional[str]]:
        """
        Validate technical question answer
        
        Args:
            answer: Answer string to validate
            min_length: Minimum required length
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not answer or not answer.strip():
            return False, "Answer cannot be empty"
        
        answer = answer.strip()
        
        if len(answer) < min_length:
            return False, f"Please provide a more detailed answer (at least {min_length} characters)"
        
        return True, None