import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from pydantic_settings import BaseSettings

class GeminiService:
    def __init__(self):
        # Configure Gemini API
        try:
            api_key = self._get_api_key()
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-2.0-flash-exp'  # Latest model
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Gemini client initialized successfully with model: {self.model_name}")
        except Exception as e:
            logging.basicConfig(level=logging.ERROR)
            self.logger = logging.getLogger(__name__)
            self.logger.error(f"Failed to initialize Gemini API: {str(e)}")
            self.client = None
    
    def _get_api_key(self) -> str:
        """Get Gemini API key from environment variables."""
        try:
            import os
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            return api_key
        except Exception as e:
            raise ValueError(f"Failed to get Gemini API key: {str(e)}")
    
    def generate_ai_response(self, prompt: str, temperature: float = 0.7) -> Optional[str]:
        """
        Generate AI response using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            temperature: Temperature for response generation (0.0 to 1.0)
            
        Returns:
            Generated text response or None if error occurs
        """
        if not self.client:
            self.logger.error("Gemini client not initialized")
            return None
        
        try:
            # Generate response using new API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                )
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                self.logger.warning("Empty response from Gemini")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating AI response: {str(e)}")
            return None
    
    def generate_structured_response(self, prompt: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate structured JSON response from Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            schema: Expected JSON structure
            
        Returns:
            Structured response as dictionary or None if error occurs
        """
        # Add JSON formatting instructions to prompt
        json_prompt = f"""
{prompt}

Please respond with a valid JSON object that follows this structure:
{json.dumps(schema, indent=2)}

Ensure your response is valid JSON that can be parsed directly.
"""
        
        response_text = self.generate_ai_response(json_prompt, temperature=0.3)
        
        if not response_text:
            return None
        
        try:
            # Try to parse JSON response
            # Clean up response if it contains markdown code blocks
            clean_response = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
            except:
                pass
            return None
    
    def is_available(self) -> bool:
        """Check if Gemini API is available and configured."""
        return self.client is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the Gemini model."""
        return {
            "model_name": self.model_name if hasattr(self, 'model_name') else "unknown",
            "available": self.is_available(),
            "api_configured": bool(self._get_api_key() if hasattr(self, '_get_api_key') else False)
        }

# Global instance
gemini_service = GeminiService()

# Helper function for easy access
def generate_ai_response(prompt: str, temperature: float = 0.7) -> Optional[str]:
    """
    Helper function to generate AI response using Gemini.
    
    Args:
        prompt: The prompt to send to Gemini
        temperature: Temperature for response generation
        
    Returns:
        Generated text response or None if error occurs
    """
    return gemini_service.generate_ai_response(prompt, temperature)

def generate_structured_response(prompt: str, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Helper function to generate structured JSON response from Gemini.
    
    Args:
        prompt: The prompt to send to Gemini
        schema: Expected JSON structure
        
    Returns:
        Structured response as dictionary or None if error occurs
    """
    return gemini_service.generate_structured_response(prompt, schema)
