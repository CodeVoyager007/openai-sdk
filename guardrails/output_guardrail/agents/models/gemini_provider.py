import google.generativeai as genai
from typing import Any, Dict, Optional
from openai_agents.models.base import BaseModelProvider

class GeminiProvider(BaseModelProvider):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate(self, prompt: str, **kwargs) -> str:
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_model_name(self) -> str:
        return "gemini/gemini-pro" 