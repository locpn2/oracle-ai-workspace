from typing import List, Dict, Optional
from .ollama import ollama_client
from ..core.config import get_settings

settings = get_settings()


class LLMProvider:
    """Router for different LLM providers"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or settings.default_llm_provider
    
    async def generate(self, prompt: str, system: str = None, 
                       temperature: float = 0.3) -> str:
        """Generate text from prompt"""
        if self.provider == "ollama":
            return await ollama_client.generate(prompt, system, temperature)
        elif self.provider == "openai":
            return await self._openai_generate(prompt, system, temperature)
        else:
            return await ollama_client.generate(prompt, system, temperature)
    
    async def chat(self, messages: List[Dict[str, str]], 
                   temperature: float = 0.3) -> str:
        """Generate from chat messages"""
        if self.provider == "ollama":
            return await ollama_client.chat(messages, temperature)
        elif self.provider == "openai":
            return await self._openai_chat(messages, temperature)
        else:
            return await ollama_client.chat(messages, temperature)
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings"""
        if self.provider == "ollama":
            return await ollama_client.embed(text)
        elif self.provider == "openai":
            return await self._openai_embed(text)
        else:
            return await ollama_client.embed(text)
    
    async def _openai_generate(self, prompt: str, system: str = None,
                               temperature: float = 0.3) -> str:
        """OpenAI text generation (placeholder)"""
        if not settings.openai_api_key:
            return ""
        # Placeholder for OpenAI integration
        return ""
    
    async def _openai_chat(self, messages: List[Dict[str, str]], 
                          temperature: float = 0.3) -> str:
        """OpenAI chat (placeholder)"""
        if not settings.openai_api_key:
            return ""
        return ""
    
    async def _openai_embed(self, text: str) -> List[float]:
        """OpenAI embeddings (placeholder)"""
        if not settings.openai_api_key:
            return []
        return []


llm_provider = LLMProvider()