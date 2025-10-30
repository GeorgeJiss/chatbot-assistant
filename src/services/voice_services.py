from gtts import gTTS
from pathlib import Path
import os
import speech_recognition as sr
from typing import Optional, Tuple
import config
import tempfile
import uuid

class VoiceService:
    """Service for voice interaction"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.audio_dir = config.AUDIO_DIR
        
    def text_to_speech(self, text: str, language: str = 'en') -> Optional[str]:
        """
        Convert text to speech and return audio file path
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            Path to audio file or None
        """
        try:
            # Clean text for TTS
            clean_text = self._clean_text_for_tts(text)
            
            # Generate unique filename
            filename = f"tts_{uuid.uuid4().hex}.mp3"
            filepath = self.audio_dir / filename
            
            # Generate speech
            tts = gTTS(text=clean_text, lang=language, slow=config.TTS_SLOW)
            tts.save(str(filepath))
            
            return str(filepath)
        
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return None
    
    def speech_to_text(
        self,
        timeout: int = config.SPEECH_TIMEOUT,
        phrase_time_limit: int = config.SPEECH_PHRASE_TIMEOUT
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Convert speech to text using microphone
        
        Args:
            timeout: Maximum time to wait for speech
            phrase_time_limit: Maximum time for a phrase
            
        Returns:
            Tuple of (success, text, error_message)
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processing speech...")
                
                # Try Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio)
                    return True, text, None
                except sr.UnknownValueError:
                    return False, None, "Could not understand audio"
                except sr.RequestError as e:
                    return False, None, f"Speech recognition service error: {e}"
        
        except Exception as e:
            return False, None, f"Error: {str(e)}"
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for better TTS output"""
        # Remove markdown formatting
        text = text.replace('**', '')
        text = text.replace('*', '')
        text = text.replace('_', '')
        text = text.replace('#', '')
        text = text.replace('`', '')
        
        # Remove emojis
        import re
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        
        # Clean up multiple spaces
        text = ' '.join(text.split())
        
        return text
    
    def cleanup_audio_files(self):
        """Remove old audio files"""
        try:
            for audio_file in self.audio_dir.glob("tts_*.mp3"):
                try:
                    audio_file.unlink()
                except:
                    pass
        except Exception as e:
            print(f"Error cleaning up audio files: {e}")
