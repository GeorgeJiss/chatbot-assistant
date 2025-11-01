# from gtts import gTTS
# from pathlib import Path
# import os
# # import speech_recognition as sr
# from typing import Optional, Tuple
# import config
# import tempfile
# import uuid
# import time

# class VoiceService:
#     """Service for voice interaction with improved recognition"""
    
#     def __init__(self):
#         self.recognizer = sr.Recognizer()
#         # Optimized settings for better recognition
#         self.recognizer.energy_threshold = 300  # Lower threshold for sensitivity
#         self.recognizer.dynamic_energy_threshold = True
#         self.recognizer.dynamic_energy_adjustment_damping = 0.15
#         self.recognizer.dynamic_energy_ratio = 1.5
#         self.recognizer.pause_threshold = 0.8  # Shorter pause detection
#         self.recognizer.phrase_threshold = 0.3
#         self.recognizer.non_speaking_duration = 0.5
#         self.audio_dir = config.AUDIO_DIR
        
#         # Test microphone on initialization
#         self._test_microphone_on_init()
    
#     def _test_microphone_on_init(self):
#         """Test microphone availability on initialization"""
#         try:
#             with sr.Microphone() as source:
#                 print("✅ Microphone detected and ready")
#         except Exception as e:
#             print(f"⚠️ Microphone warning: {e}")
    
#     def text_to_speech(self, text: str, language: str = 'en') -> Optional[str]:
#         """
#         Convert text to speech and return audio file path
        
#         Args:
#             text: Text to convert
#             language: Language code
            
#         Returns:
#             Path to audio file or None
#         """
#         try:
#             # Clean text for TTS
#             clean_text = self._clean_text_for_tts(text)
            
#             if not clean_text.strip():
#                 return None
            
#             # Generate unique filename
#             filename = f"tts_{uuid.uuid4().hex}.mp3"
#             filepath = self.audio_dir / filename
            
#             # Generate speech with retry logic
#             max_retries = 3
#             for attempt in range(max_retries):
#                 try:
#                     tts = gTTS(text=clean_text, lang=language, slow=config.TTS_SLOW)
#                     tts.save(str(filepath))
#                     print(f"✅ Audio generated: {filepath}")
#                     return str(filepath)
#                 except Exception as e:
#                     if attempt < max_retries - 1:
#                         time.sleep(1)
#                         continue
#                     else:
#                         print(f"❌ Error in text-to-speech after {max_retries} attempts: {e}")
#                         return None
        
#         except Exception as e:
#             print(f"❌ Error in text-to-speech: {e}")
#             return None
    
#     def speech_to_text(
#         self,
#         timeout: int = None,
#         phrase_time_limit: int = None
#     ) -> Tuple[bool, Optional[str], Optional[str]]:
#         """
#         Convert speech to text using microphone with improved error handling
        
#         Args:
#             timeout: Maximum time to wait for speech (default from config)
#             phrase_time_limit: Maximum time for a phrase (default from config)
            
#         Returns:
#             Tuple of (success, text, error_message)
#         """
#         if timeout is None:
#             timeout = config.SPEECH_TIMEOUT
#         if phrase_time_limit is None:
#             phrase_time_limit = config.SPEECH_PHRASE_TIMEOUT
        
#         try:
#             # List available microphones for debugging
#             mic_list = sr.Microphone.list_microphone_names()
#             print(f"Available microphones: {len(mic_list)}")
#             for index, name in enumerate(mic_list):
#                 print(f"  [{index}] {name}")
            
#             # Use default microphone
#             with sr.Microphone() as source:
#                 print("✅ Microphone initialized successfully")
                
#                 # Adjust for ambient noise - SHORTER duration
#                 print("🔧 Calibrating for ambient noise... (0.5 seconds)")
#                 self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
#                 print(f"🎤 Ready to listen (timeout: {timeout}s, phrase limit: {phrase_time_limit}s)")
#                 print(f"📊 Energy threshold: {self.recognizer.energy_threshold}")
                
#                 try:
#                     # Listen for audio
#                     print("👂 Listening now...")
#                     audio = self.recognizer.listen(
#                         source,
#                         timeout=timeout,
#                         phrase_time_limit=phrase_time_limit
#                     )
                    
#                     print("✅ Audio captured! Processing...")
                    
#                     # Try Google Speech Recognition first
#                     try:
#                         text = self.recognizer.recognize_google(audio)
#                         print(f"✅ Recognized: '{text}'")
                        
#                         if not text or len(text.strip()) == 0:
#                             return False, None, "No speech detected. Please try again."
                        
#                         return True, text, None
                        
#                     except sr.UnknownValueError:
#                         print("❌ Could not understand audio")
                        
#                         # Try alternative: recognize_google with different language
#                         try:
#                             text = self.recognizer.recognize_google(audio, language="en-IN")
#                             print(f"✅ Recognized (alt): '{text}'")
#                             return True, text, None
#                         except:
#                             pass
                        
#                         return False, None, "Could not understand the audio. Please speak clearly and try again."
                        
#                     except sr.RequestError as e:
#                         print(f"❌ Speech recognition service error: {e}")
#                         return False, None, "Speech recognition service error. Please check your internet connection."
                
#                 except sr.WaitTimeoutError:
#                     print("❌ Listening timed out - no speech detected")
#                     return False, None, f"No speech detected within {timeout} seconds. Please try again."
        
#         except OSError as e:
#             error_msg = str(e)
#             print(f"❌ Microphone OS error: {error_msg}")
            
#             if "No Default Input Device Available" in error_msg or "device" in error_msg.lower():
#                 return False, None, "❌ No microphone detected. Please:\n1. Connect a microphone\n2. Check system permissions\n3. Refresh the page"
            
#             return False, None, f"Microphone error: {error_msg}. Please check your microphone connection."
        
#         except Exception as e:
#             print(f"❌ Unexpected error in speech_to_text: {type(e).__name__}: {e}")
#             return False, None, f"Unexpected error: {str(e)}. Please try again or use text input."
    
#     def test_microphone(self) -> Tuple[bool, str]:
#         """
#         Test if microphone is working
        
#         Returns:
#             Tuple of (is_working, message)
#         """
#         try:
#             mic_list = sr.Microphone.list_microphone_names()
            
#             if len(mic_list) == 0:
#                 return False, "❌ No microphone devices found on your system."
            
#             print(f"Found {len(mic_list)} microphone(s)")
            
#             with sr.Microphone() as source:
#                 self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
#                 print(f"Microphone energy threshold: {self.recognizer.energy_threshold}")
                
#             return True, f"✅ Microphone is working! Found {len(mic_list)} device(s)."
            
#         except OSError as e:
#             return False, f"❌ Microphone not accessible: {str(e)}\n\nPlease check:\n1. Microphone is connected\n2. System permissions granted\n3. No other app is using it"
            
#         except Exception as e:
#             return False, f"❌ Microphone test failed: {str(e)}"
    
#     def _clean_text_for_tts(self, text: str) -> str:
#         """Clean text for better TTS output"""
#         # Remove markdown formatting
#         import re
        
#         text = text.replace('**', '')
#         text = text.replace('*', '')
#         text = text.replace('_', '')
#         text = text.replace('#', '')
#         text = text.replace('`', '')
        
#         # Remove specific formatting patterns
#         text = text.replace("Technology:", "Technology:")
#         text = text.replace("Question:", "Question:")
#         text = text.replace("Technical Question", "Question")
        
#         # Remove URLs
#         text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
#         # Remove emojis
#         emoji_pattern = re.compile("["
#             u"\U0001F600-\U0001F64F"  # emoticons
#             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#             u"\U0001F680-\U0001F6FF"  # transport & map symbols
#             u"\U0001F1E0-\U0001F1FF"  # flags
#             u"\U00002702-\U000027B0"
#             u"\U000024C2-\U0001F251"
#             "]+", flags=re.UNICODE)
#         text = emoji_pattern.sub(r'', text)
        
#         # Clean up multiple spaces
#         text = ' '.join(text.split())
        
#         # Limit length for TTS (prevent timeout)
#         if len(text) > 500:
#             # Try to cut at sentence boundary
#             sentences = text.split('.')
#             text = ''
#             for sentence in sentences:
#                 if len(text) + len(sentence) < 497:
#                     text += sentence + '.'
#                 else:
#                     break
            
#             if len(text) > 500:
#                 text = text[:497] + "..."
        
#         return text
    
#     def cleanup_audio_files(self, max_age_hours: int = 1):
#         """
#         Remove old audio files
        
#         Args:
#             max_age_hours: Maximum age of files to keep in hours
#         """
#         try:
#             current_time = time.time()
#             max_age_seconds = max_age_hours * 3600
            
#             deleted_count = 0
#             for audio_file in self.audio_dir.glob("tts_*.mp3"):
#                 try:
#                     file_age = current_time - audio_file.stat().st_mtime
#                     if file_age > max_age_seconds:
#                         audio_file.unlink()
#                         deleted_count += 1
#                 except Exception as e:
#                     print(f"Could not delete {audio_file}: {e}")
            
#             if deleted_count > 0:
#                 print(f"🧹 Cleaned up {deleted_count} old audio files")
                
#         except Exception as e:
#             print(f"Error cleaning up audio files: {e}")
    
#     def get_microphone_info(self) -> dict:
#         """Get information about available microphones"""
#         try:
#             mic_list = sr.Microphone.list_microphone_names()
            
#             return {
#                 'count': len(mic_list),
#                 'devices': mic_list,
#                 'default_available': len(mic_list) > 0
#             }
#         except Exception as e:
#             return {
#                 'count': 0,
#                 'devices': [],
#                 'default_available': False,
#                 'error': str(e)
#             }

"""
Voice service - DISABLED
This is a placeholder file. Voice features have been removed.
"""

class VoiceService:
    """Placeholder class - voice features disabled"""
    
    def __init__(self):
        pass
    
    def text_to_speech(self, text: str, language: str = 'en'):
        """Disabled"""
        return None
    
    def speech_to_text(self):
        """Disabled"""
        return False, None, "Voice features are disabled"