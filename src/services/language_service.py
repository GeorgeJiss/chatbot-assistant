from langdetect import detect, LangDetectException
from typing import Optional, Dict
import config

class LanguageService:
    """Service for multilingual support"""
    
    def __init__(self):
        self.supported_languages = config.SUPPORTED_LANGUAGES
        self.translations = self._load_translations()
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code or None
        """
        try:
            lang = detect(text)
            return lang if lang in self.supported_languages else 'en'
        except LangDetectException:
            return 'en'  # Default to English
    
    def _load_translations(self) -> Dict:
        """Load translation templates"""
        return {
            'en': {
                'greeting': "Hello! Welcome to TalentScout AI Voice Interviewer.",
                'name_prompt': "Please tell me your full name.",
                'email_prompt': "What is your email address?",
                'experience_prompt': "How many years of professional experience do you have?",
                'tech_stack_prompt': "Please tell me the technologies you're proficient in.",
                'question_intro': "I will now ask you technical questions.",
                'waiting': "I'm waiting for your response.",
                'timeout': "I didn't hear a response. Let's continue.",
                'thank_you': "Thank you for your time!",
                'invalid_answer': "I couldn't quite understand that. Could you please rephrase?",
            },
            'es': {
                'greeting': "Hola! Bienvenido al Entrevistador de Voz TalentScout AI.",
                'name_prompt': "Por favor dígame su nombre completo.",
                'email_prompt': "Cuál es su dirección de correo electrónico?",
                'experience_prompt': "Cuántos años de experiencia profesional tiene?",
                'tech_stack_prompt': "Por favor dígame las tecnologías en las que es competente.",
                'question_intro': "Ahora le haré preguntas técnicas.",
                'waiting': "Estoy esperando su respuesta.",
                'timeout': "No escuché una respuesta. Continuemos.",
                'thank_you': "Gracias por su tiempo!",
                'invalid_answer': "No pude entender eso. Podría reformularlo?",
            },
            'hi': {
                'greeting': "नमस्ते! TalentScout AI वॉयस इंटरव्यूअर में आपका स्वागत है।",
                'name_prompt': "कृपया मुझे अपना पूरा नाम बताएं।",
                'email_prompt': "आपका ईमेल पता क्या है?",
                'experience_prompt': "आपके पास कितने वर्षों का पेशेवर अनुभव है?",
                'tech_stack_prompt': "कृपया मुझे उन तकनीकों के बारे में बताएं जिनमें आप कुशल हैं।",
                'question_intro': "अब मैं आपसे तकनीकी प्रश्न पूछूंगा।",
                'waiting': "मैं आपके जवाब का इंतजार कर रहा हूं।",
                'timeout': "मुझे कोई जवाब नहीं सुनाई दिया। चलिए आगे बढ़ते हैं।",
                'thank_you': "आपके समय के लिए धन्यवाद!",
                'invalid_answer': "मैं वह समझ नहीं पाया। क्या आप फिर से कह सकते हैं?",
            }
        }
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text"""
        return self.translations.get(language, self.translations['en']).get(key, key)
    
    def translate_question(self, question: str, target_lang: str) -> str:
        """
        Translate question to target language
        Note: This is a placeholder. In production, use proper translation API
        
        Args:
            question: Question in English
            target_lang: Target language code
            
        Returns:
            Translated question (or original if translation not available)
        """
        return question