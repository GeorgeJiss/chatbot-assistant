from typing import List, Dict, Optional
import config
from src.services.llm_service import LLMService
from src.utils.helpers import categorize_technology, get_experience_level, get_difficulty_from_role

class QuestionGenerator:
    """Generate technical questions based on role, experience, and tech stack"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.questions_per_tech = config.QUESTIONS_PER_TECH
        self.question_cache = {}
    
    def generate_questions_for_tech(
        self,
        technology: str,
        role: str = "",
        experience_years: float = 0,
        num_questions: int = None
    ) -> List[str]:
        """
        Generate technical questions for a specific technology based on role and experience
        
        Args:
            technology: Technology name (e.g., 'Python', 'React')
            role: Job role (e.g., 'Senior Developer', 'Junior Engineer')
            experience_years: Years of experience
            num_questions: Number of questions to generate
            
        Returns:
            List of tailored technical questions
        """
        if num_questions is None:
            num_questions = self.questions_per_tech
        
        # Determine difficulty level from role and experience
        difficulty = self._determine_difficulty(role, experience_years)
        
        # Get technology category for context
        category = categorize_technology(technology)
        
        # Create cache key
        cache_key = f"{technology.lower()}_{difficulty}_{num_questions}"
        
        # Check cache
        if cache_key in self.question_cache:
            print(f"📦 Using cached questions for {technology} at {difficulty} level")
            return self.question_cache[cache_key]
        
        # Build comprehensive prompt
        system_prompt = self._build_system_prompt(
            technology, 
            difficulty, 
            role, 
            category,
            num_questions
        )
        
        user_prompt = f"""Generate {num_questions} technical interview questions for {technology}.

Requirements:
- Target level: {difficulty}
- Role context: {role if role else 'General Developer'}
- Each question should test a different aspect
- Include both theoretical and practical questions
- Make questions specific to {technology}, not generic

Format: Return ONLY the questions, numbered 1., 2., 3., etc."""
        
        # Generate questions using LLM
        print(f"🔄 Generating {num_questions} {difficulty}-level questions for {technology}...")
        response = self.llm_service.generate_response(
            user_prompt,
            system_message=system_prompt,
            temperature=0.8,
            max_tokens=800
        )
        
        if not response:
            print(f"⚠️ LLM generation failed, using fallback questions for {technology}")
            return self._get_fallback_questions(technology, difficulty, num_questions)
        
        # Parse response into list of questions
        questions = self._parse_questions(response)
        
        # Ensure we have the right number of questions
        if len(questions) < num_questions:
            print(f"⚠️ Only got {len(questions)} questions, generating more...")
            fallback = self._get_fallback_questions(
                technology,
                difficulty,
                num_questions - len(questions)
            )
            questions.extend(fallback)
        
        # Take only the requested number
        questions = questions[:num_questions]
        
        # Cache the questions
        self.question_cache[cache_key] = questions
        
        print(f"✅ Generated {len(questions)} questions for {technology}")
        return questions
    
    def _determine_difficulty(self, role: str, experience_years: float) -> str:
        """Determine difficulty level from role and experience"""
        # First try to get difficulty from role
        if role:
            difficulty = get_difficulty_from_role(role)
            if difficulty:
                return difficulty
        
        # Fallback to experience level
        return get_experience_level(experience_years)
    
    def _build_system_prompt(
        self, 
        technology: str, 
        difficulty: str, 
        role: str,
        category: str,
        num_questions: int
    ) -> str:
        """Build comprehensive system prompt for question generation"""
        
        difficulty_guidelines = {
            "junior": """
- Focus on fundamental concepts and basic syntax
- Test understanding of core features
- Include simple practical scenarios
- Ask about common use cases
- Avoid advanced architectural questions
""",
            "mid": """
- Test practical application and problem-solving
- Include real-world scenarios and debugging
- Cover intermediate concepts and patterns
- Ask about best practices
- Test understanding of ecosystem and tools
""",
            "senior": """
- Focus on advanced concepts and optimization
- Test architectural decision-making
- Include complex problem-solving scenarios
- Ask about performance, scalability, and security
- Cover design patterns and system design
""",
            "architect": """
- Focus on system architecture and design
- Test strategic technical decisions
- Include scalability and infrastructure questions
- Ask about trade-offs and best practices
- Cover team leadership and technical direction
"""
        }
        
        return f"""You are an expert technical interviewer specializing in {technology}.

Context:
- Technology: {technology}
- Category: {category}
- Difficulty Level: {difficulty}
- Role: {role if role else 'General Developer'}

Your task is to generate {num_questions} high-quality technical interview questions.

Guidelines for {difficulty} level:
{difficulty_guidelines.get(difficulty, difficulty_guidelines['mid'])}

Question Quality Requirements:
1. Questions must be specific to {technology}
2. Each question should test different knowledge areas
3. Mix of conceptual understanding and practical application
4. Clear, concise, and unambiguous wording
5. Relevant to real-world development scenarios

Format: Return only the questions, numbered 1., 2., 3., etc.
Do NOT include answers, explanations, or any additional text."""
    
    def _parse_questions(self, text: str) -> List[str]:
        """Parse questions from LLM response"""
        questions = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Remove numbering (1., 2., Q1:, etc.)
            if line[0].isdigit() or line.startswith('Q'):
                # Find the question text after numbering
                for separator in ['. ', ': ', ') ', '- ']:
                    if separator in line:
                        parts = line.split(separator, 1)
                        if len(parts) > 1:
                            question = parts[1].strip()
                            break
                else:
                    question = line
            else:
                question = line
            
            # Validate question
            if self._is_valid_question(question):
                questions.append(question)
        
        return questions
    
    def _is_valid_question(self, text: str) -> bool:
        """Validate if text is a proper question"""
        # Must be reasonable length
        if len(text) < 15 or len(text) > 500:
            return False
        
        # Should contain question indicators
        question_indicators = ['?', 'what', 'how', 'why', 'explain', 'describe', 'when', 'which']
        text_lower = text.lower()
        
        has_indicator = any(indicator in text_lower for indicator in question_indicators)
        
        # Should not be an answer or explanation
        answer_indicators = ['answer:', 'solution:', 'response:', 'because', 'therefore']
        is_answer = any(indicator in text_lower for indicator in answer_indicators)
        
        return has_indicator and not is_answer
    
    def _get_fallback_questions(
        self,
        technology: str,
        difficulty: str,
        num_questions: int
    ) -> List[str]:
        """Get fallback questions when LLM fails"""
        
        # Technology-specific question templates
        question_templates = {
            "junior": [
                f"What are the main features of {technology}?",
                f"Can you explain the basic syntax of {technology}?",
                f"What is {technology} commonly used for?",
                f"How do you get started with {technology}?",
                f"What are the advantages of using {technology}?",
            ],
            "mid": [
                f"Explain the key concepts and architecture of {technology}.",
                f"What are some best practices when working with {technology}?",
                f"Describe a challenging problem you solved using {technology}.",
                f"How does {technology} handle error handling and debugging?",
                f"What are the common pitfalls when using {technology}?",
            ],
            "senior": [
                f"How would you optimize performance in a {technology} application?",
                f"Explain the design patterns commonly used with {technology}.",
                f"How do you ensure scalability when working with {technology}?",
                f"What are the security considerations for {technology}?",
                f"Compare {technology} with similar technologies and explain when to use each.",
            ],
            "architect": [
                f"How would you design a large-scale system using {technology}?",
                f"What architectural decisions would you make when choosing {technology}?",
                f"Explain how you would integrate {technology} in a microservices architecture.",
                f"What are the trade-offs of using {technology} at enterprise scale?",
                f"How would you mentor a team to adopt {technology} effectively?",
            ]
        }
        
        templates = question_templates.get(difficulty, question_templates['mid'])
        return templates[:num_questions]
    
    def generate_all_questions(
        self,
        tech_stack: List[str],
        role: str = "",
        experience_years: float = 0
    ) -> Dict[str, List[str]]:
        """
        Generate questions for entire tech stack
        
        Args:
            tech_stack: List of technologies
            role: Job role
            experience_years: Years of experience
            
        Returns:
            Dictionary mapping technology to questions
        """
        all_questions = {}
        
        print(f"\n{'='*60}")
        print(f"Generating questions for role: {role}")
        print(f"Experience: {experience_years} years")
        print(f"Tech stack: {', '.join(tech_stack)}")
        print(f"{'='*60}\n")
        
        for tech in tech_stack:
            questions = self.generate_questions_for_tech(
                tech,
                role=role,
                experience_years=experience_years
            )
            all_questions[tech] = questions
        
        return all_questions
    
    def format_question(
        self,
        technology: str,
        question: str,
        question_number: int,
        total_questions: int
    ) -> str:
        """Format question for display"""
        return f"""**Question {question_number} of {total_questions}**

**Technology:** {technology.title()}

**Question:** {question}

Please provide your answer below."""