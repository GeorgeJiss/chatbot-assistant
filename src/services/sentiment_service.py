from textblob import TextBlob
from typing import Dict, Tuple
import config

class SentimentService:
    """Service for analyzing sentiment and answer quality"""
    
    def __init__(self):
        pass
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with polarity and subjectivity
        """
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            return {
                'polarity': sentiment.polarity,  # -1 to 1 (negative to positive)
                'subjectivity': sentiment.subjectivity,  # 0 to 1 (objective to subjective)
                'assessment': self._assess_sentiment(sentiment.polarity)
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'polarity': 0.0,
                'subjectivity': 0.5,
                'assessment': 'neutral'
            }
    
    def _assess_sentiment(self, polarity: float) -> str:
        """Assess sentiment based on polarity"""
        if polarity > 0.3:
            return 'positive'
        elif polarity < -0.3:
            return 'negative'
        else:
            return 'neutral'
    
    def validate_answer_quality(self, answer: str, question: str) -> Tuple[bool, str, Dict]:
        """
        Validate if answer makes sense for the question
        
        Args:
            answer: Candidate's answer
            question: Original question
            
        Returns:
            Tuple of (is_valid, message, metrics)
        """
        metrics = {
            'length': len(answer),
            'word_count': len(answer.split()),
            'sentiment': self.analyze_sentiment(answer)
        }
        
        # Check minimum length
        if len(answer) < config.MIN_ANSWER_LENGTH:
            return False, "Your answer seems too short. Please provide more detail.", metrics
        
        # Check maximum length
        if len(answer) > config.MAX_ANSWER_LENGTH:
            return False, "Your answer is too long. Please be more concise.", metrics
        
        # Check if answer is just repetition
        words = answer.lower().split()
        if len(words) > 0 and len(set(words)) / len(words) < 0.3:
            return False, "Your answer seems repetitive. Please provide a more varied response.", metrics
        
        # Check sentiment - extreme negativity might indicate confusion or frustration
        if metrics['sentiment']['polarity'] < config.SENTIMENT_THRESHOLD:
            return True, "I notice you might be uncertain. That's okay, please share what you know.", metrics
        
        # Check if answer contains question keywords (relevance)
        question_keywords = set(question.lower().split())
        answer_keywords = set(answer.lower().split())
        overlap = len(question_keywords.intersection(answer_keywords))
        
        if overlap == 0 and len(answer.split()) > 5:
            return True, "Please try to address the specific question asked.", metrics
        
        return True, "Answer recorded.", metrics
    
    def check_answer_relevance(self, answer: str, question: str, technology: str) -> float:
        """
        Check how relevant the answer is to the question
        
        Args:
            answer: Candidate's answer
            question: Original question
            technology: Technology being assessed
            
        Returns:
            Relevance score (0-1)
        """
        try:
            # Simple keyword matching
            tech_in_answer = technology.lower() in answer.lower()
            
            # Extract important words from question
            question_words = set(word.lower() for word in question.split() 
                               if len(word) > 3 and word.isalnum())
            answer_words = set(word.lower() for word in answer.split() 
                             if len(word) > 3 and word.isalnum())
            
            # Calculate overlap
            overlap = len(question_words.intersection(answer_words))
            relevance = overlap / len(question_words) if question_words else 0
            
            # Boost if technology mentioned
            if tech_in_answer:
                relevance = min(1.0, relevance + 0.2)
            
            return relevance
        
        except Exception as e:
            print(f"Error checking relevance: {e}")
            return 0.5
    
    def generate_feedback(self, metrics: Dict) -> str:
        """Generate feedback based on answer metrics"""
        sentiment = metrics['sentiment']['assessment']
        word_count = metrics['word_count']
        
        feedback = []
        
        if word_count < 10:
            feedback.append("Consider providing more detail in your answers.")
        elif word_count > 150:
            feedback.append("Try to be more concise in your responses.")
        
        if sentiment == 'negative':
            feedback.append("I sense some uncertainty. Remember, it's okay to say what you know.")
        elif sentiment == 'positive':
            feedback.append("Great confidence in your answer!")
        
        return " ".join(feedback) if feedback else "Thank you for your response."