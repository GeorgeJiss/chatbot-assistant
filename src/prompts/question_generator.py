from typing import List, Dict
import config
from src.services.llm_service import LLMService
from src.utils.helpers import categorize_technology, get_experience_level

class QuestionGenerator:
    """Generate technical questions based on candidate's tech stack"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.questions_per_tech = config.QUESTIONS_PER_TECH
    
    def generate_questions_for_tech(
        self,
        technology: str,
        experience_years: float = 0,
        num_questions: int = None
    ) -> List[str]:
        """
        Generate technical questions for a specific technology
        
        Args:
            technology: Technology name
            experience_years: Candidate's years of experience
            num_questions: Number of questions to generate
            
        Returns:
            List of questions
        """
        if num_questions is None:
            num_questions = self.questions_per_tech
        
        # Determine difficulty based on experience
        experience_level = get_experience_level(experience_years)
        
        difficulty_descriptions = {
            "junior": "entry-level to intermediate",
            "mid": "intermediate to advanced",
            "senior": "advanced to expert-level",
            "lead": "expert-level and architectural"
        }
        
        difficulty = difficulty_descriptions.get(experience_level, "intermediate")
        
        # Get technology category
        category = categorize_technology(technology)
        
        # Create prompt for question generation
        system_prompt = f"""You are a technical interviewer creating screening questions.

Generate {num_questions} technical questions for {technology}.

Requirements:
- Questions should be {difficulty} difficulty level
- Focus on practical knowledge and real-world scenarios
- Questions should be specific to {technology}
- Include a mix of conceptual and practical questions
- Keep questions clear and concise
- Each question should assess different aspects of the technology

Format: Return ONLY the questions, numbered 1., 2., 3., etc.
Do not include answers or explanations."""

        user_prompt = f"Generate {num_questions} {difficulty} technical interview questions about {technology}."
        
        # Generate questions using LLM
        response = self.llm_service.generate_response(
            user_prompt,
            system_message=system_prompt,
            temperature=0.8
        )
        
        if not response:
            # Fallback to template questions
            return self._get_fallback_questions(technology, num_questions)
        
        # Parse response into list of questions
        questions = self._parse_questions(response)
        
        # Ensure we have the right number of questions
        if len(questions) < num_questions:
            questions.extend(
                self._get_fallback_questions(
                    technology,
                    num_questions - len(questions)
                )
            )
        
        return questions[:num_questions]
    
    def _parse_questions(self, text: str) -> List[str]:
        """Parse questions from text response"""
        questions = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Remove numbering (1., 2., etc.)
            if line and line[0].isdigit():
                # Find the first non-digit, non-dot, non-space character
                idx = 0
                for i, char in enumerate(line):
                    if char not in '0123456789. ':
                        idx = i
                        break
                
                question = line[idx:].strip()
                if question and len(question) > 10:
                    questions.append(question)
            elif line and len(line) > 10:
                questions.append(line)
        
        return questions
    
    def _get_fallback_questions(
        self,
        technology: str,
        num_questions: int
    ) -> List[str]:
        """Get fallback template questions if LLM fails"""
        templates = [
            f"Can you explain the key features and use cases of {technology}?",
            f"What are some best practices you follow when working with {technology}?",
            f"Describe a challenging problem you solved using {technology}.",
            f"How does {technology} compare to similar technologies you've used?",
            f"What are the main advantages and limitations of {technology}?",
        ]
        
        return templates[:num_questions]
    
    def generate_all_questions(
        self,
        tech_stack: List[str],
        experience_years: float = 0
    ) -> Dict[str, List[str]]:
        """
        Generate questions for entire tech stack
        
        Args:
            tech_stack: List of technologies
            experience_years: Candidate's years of experience
            
        Returns:
            Dictionary mapping technology to list of questions
        """
        all_questions = {}
        
        for tech in tech_stack:
            questions = self.generate_questions_for_tech(
                tech,
                experience_years
            )
            all_questions[tech] = questions
        
        return all_questions
    
    def get_next_question(
        self,
        tech_stack: List[str],
        answered_questions: Dict[str, List[str]],
        experience_years: float = 0
    ) -> tuple:
        """
        Get the next question to ask
        
        Args:
            tech_stack: List of technologies
            answered_questions: Dict of tech -> list of answered questions
            experience_years: Candidate's years of experience
            
        Returns:
            Tuple of (technology, question) or (None, None) if all done
        """
        for tech in tech_stack:
            # Check how many questions have been answered for this tech
            answered_count = len(answered_questions.get(tech, []))
            
            if answered_count < self.questions_per_tech:
                # Generate question if not already generated
                if tech not in answered_questions:
                    questions = self.generate_questions_for_tech(
                        tech,
                        experience_years
                    )
                    answered_questions[tech] = []
                    
                    # Return first question
                    if questions:
                        return tech, questions[0]
                else:
                    # Get all questions for this tech
                    all_questions = self.generate_questions_for_tech(
                        tech,
                        experience_years
                    )
                    
                    # Find next unanswered question
                    for q in all_questions:
                        if q not in answered_questions[tech]:
                            return tech, q
        
        # All questions answered
        return None, None
    
    def format_question(
        self,
        technology: str,
        question: str,
        question_number: int,
        total_questions: int
    ) -> str:
        """
        Format a question for display
        
        Args:
            technology: Technology name
            question: Question text
            question_number: Current question number
            total_questions: Total number of questions
            
        Returns:
            Formatted question string
        """
        return f"""**Technical Question {question_number}/{total_questions}**

**Technology:** {technology.title()}

**Question:** {question}

Please provide your answer below."""