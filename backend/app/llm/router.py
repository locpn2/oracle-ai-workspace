from typing import List, Dict, Optional
import re
import aiohttp
from .ollama import ollama_client
from ..core.config import get_settings

settings = get_settings()

OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OPENAI_EMBED_MODEL = "text-embedding-3-small"

SIMPLE_QUERY_PATTERNS = [
    r"^(show|list|get|find|display)\s+",
    r"^count\s+",
    r"^how many\s+",
    r"^total\s+",
]


def classify_query_complexity(natural_language: str) -> str:
    """Classify query as 'simple' or 'complex'"""
    nl_lower = natural_language.lower().strip()
    for pattern in SIMPLE_QUERY_PATTERNS:
        if re.search(pattern, nl_lower):
            return "simple"
    return "complex"


class LLMProvider:
    """Router for different LLM providers with smart fallback"""

    def __init__(self, provider: str = None):
        self.provider = provider or settings.default_llm_provider

    async def chat(self, messages: List[Dict[str, str]],
                   temperature: float = 0.3,
                   query_hint: str = None) -> str:
        """Smart routing: Ollama small model -> Ollama large -> OpenAI"""

        # If query_hint provided, use smart routing
        if query_hint and self.provider == "ollama":
            return await self._smart_chat(messages, temperature, query_hint)

        return await self._direct_chat(messages, temperature)

    async def _smart_chat(self, messages: List[Dict[str, str]],
                          temperature: float, query_hint: str) -> str:
        """Route to best provider based on query complexity"""
        complexity = classify_query_complexity(query_hint)

        if complexity == "simple":
            # Try Ollama small model first (fast)
            result = await ollama_client.chat(
                messages, temperature, model=ollama_client.small_model
            )
            if result:
                return result

        # Try Ollama large model
        result = await ollama_client.chat(messages, temperature)
        if result:
            return result

        # Fallback to OpenAI if available
        if settings.openai_api_key:
            result = await self._openai_chat(messages, temperature)
            if result:
                return result

        return ""

    async def _direct_chat(self, messages: List[Dict[str, str]],
                           temperature: float) -> str:
        """Direct routing based on configured provider"""
        if self.provider == "ollama":
            return await ollama_client.chat(messages, temperature)
        elif self.provider == "openai":
            return await self._openai_chat(messages, temperature)
        else:
            return await ollama_client.chat(messages, temperature)

    async def generate(self, prompt: str, system: str = None,
                       temperature: float = 0.3) -> str:
        """Generate text from prompt"""
        if self.provider == "ollama":
            return await ollama_client.generate(prompt, system, temperature)
        elif self.provider == "openai":
            return await self._openai_generate(prompt, system, temperature)
        else:
            return await ollama_client.generate(prompt, system, temperature)

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
        """OpenAI text generation"""
        if not settings.openai_api_key:
            print("OpenAI API key not configured")
            return ""

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        return await self._openai_chat(messages, temperature)

    async def _openai_chat(self, messages: List[Dict[str, str]],
                           temperature: float = 0.3) -> str:
        """OpenAI chat completion"""
        if not settings.openai_api_key:
            print("OpenAI API key not configured")
            return ""

        try:
            headers = {
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": DEFAULT_OPENAI_MODEL,
                "messages": messages,
                "temperature": temperature
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{OPENAI_BASE_URL}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error = await response.text()
                        print(f"OpenAI API error: {response.status} - {error}")
                        return ""
        except Exception as e:
            print(f"Error calling OpenAI chat: {e}")
            return ""

    async def _openai_embed(self, text: str) -> List[float]:
        """OpenAI embeddings"""
        if not settings.openai_api_key:
            print("OpenAI API key not configured")
            return []

        try:
            headers = {
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": DEFAULT_OPENAI_EMBED_MODEL,
                "input": text
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{OPENAI_BASE_URL}/embeddings",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["data"][0]["embedding"]
                    else:
                        error = await response.text()
                        print(f"OpenAI API error: {response.status} - {error}")
                        return []
        except Exception as e:
            print(f"Error calling OpenAI embeddings: {e}")
            return []


llm_provider = LLMProvider()
