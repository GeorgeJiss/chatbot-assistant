import requests
import time
from typing import Optional, Dict, List
import config

class LLMService:
    """Service for interacting with Groq LLM API"""
    
    def __init__(self):
        self.api_key = config.GROQ_API_KEY
        self.model = config.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file.\n"
                "Get your free API key at: https://console.groq.com/"
            )
    
    def generate_response(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: int = config.MAX_TOKENS,
        temperature: float = config.TEMPERATURE,
        max_retries: int = 3
    ) -> Optional[str]:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_message: System message for context
            max_tokens: Maximum tokens in response
            temperature: Temperature for randomness
            max_retries: Maximum retry attempts
            
        Returns:
            Generated response or None on failure
        """
        messages = []
        
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": config.TOP_P
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content'].strip()
                
                elif response.status_code == 429:
                    # Rate limit - wait and retry
                    wait_time = 2 ** attempt
                    print(f"Rate limit hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return None
            
            except requests.exceptions.Timeout:
                print(f"Request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
            
            except Exception as e:
                print(f"Error generating response: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None
        
        return None
    
    def generate_with_context(
        self,
        prompt: str,
        conversation_history: List[Dict[str, str]],
        system_message: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate response with conversation context
        
        Args:
            prompt: Current user prompt
            conversation_history: List of previous messages
            system_message: System message
            
        Returns:
            Generated response or None
        """
        messages = []
        
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        # Add conversation history (limited to last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": config.MAX_TOKENS,
            "temperature": config.TEMPERATURE,
            "top_p": config.TOP_P
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                print(f"API Error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def extract_information(
        self,
        text: str,
        info_type: str
    ) -> Optional[str]:
        """
        Extract specific information from text using LLM
        
        Args:
            text: Text to extract from
            info_type: Type of information to extract
            
        Returns:
            Extracted information or None
        """
        system_message = f"""You are a data extraction assistant. 
Extract only the {info_type} from the user's message. 
Return ONLY the extracted value, nothing else.
If the information is not present, return 'NOT_FOUND'."""
        
        response = self.generate_response(
            text,
            system_message=system_message,
            temperature=0.3
        )
        
        if response and response != "NOT_FOUND":
            return response.strip()
        
        return None
    
    def check_api_health(self) -> bool:
        """
        Check if Groq API is accessible
        
        Returns:
            True if API is working, False otherwise
        """
        try:
            response = self.generate_response(
                "Say 'OK'",
                system_message="You are a test assistant. Respond with exactly 'OK'.",
                max_tokens=10
            )
            return response is not None
        except:
            return False