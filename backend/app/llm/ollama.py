from typing import List, Optional, Dict, Any
import aiohttp
from ..core.config import get_settings

settings = get_settings()


class OllamaClient:
    """Client for Ollama API with connection pooling"""

    _session: Optional[aiohttp.ClientSession] = None

    def __init__(self, base_url: str = None, model: str = None,
                 embed_model: str = None):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.small_model = settings.ollama_small_model
        self.embed_model = embed_model or settings.ollama_embed_model
        self.timeout = settings.llm_ollama_timeout

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            self._session = aiohttp.ClientSession(connector=connector)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def generate(self, prompt: str, system: str = None,
                       temperature: float = 0.3, max_tokens: int = 500,
                       model: str = None) -> str:
        """Generate text using /api/generate endpoint"""
        try:
            session = await self._get_session()
            payload = {
                "model": model or self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            if system:
                payload["system"] = system

            async with session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "")
                else:
                    error = await response.text()
                    raise Exception(f"Ollama error: {response.status} - {error}")
        except Exception as e:
            print(f"Error generating with Ollama: {e}")
            return ""

    async def chat(self, messages: List[Dict[str, str]],
                   temperature: float = 0.3, model: str = None) -> str:
        """Generate using chat endpoint"""
        try:
            session = await self._get_session()
            payload = {
                "model": model or self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }

            async with session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("message", {}).get("content", "")
                else:
                    error = await response.text()
                    raise Exception(f"Ollama error: {response.status} - {error}")
        except Exception as e:
            print(f"Error in chat with Ollama: {e}")
            return ""

    async def embed(self, text: str) -> List[float]:
        """Generate embeddings using /api/embeddings endpoint"""
        try:
            session = await self._get_session()
            payload = {
                "model": self.embed_model,
                "prompt": text
            }

            async with session.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("embedding", [])
                else:
                    error = await response.text()
                    raise Exception(f"Ollama error: {response.status} - {error}")
        except Exception as e:
            print(f"Error generating embedding with Ollama: {e}")
            return []

    async def list_models(self) -> List[str]:
        """List available models"""
        try:
            session = await self._get_session()
            async with session.get(
                f"{self.base_url}/api/tags",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return [m.get("name", "").split(":")[0] for m in result.get("models", [])]
                return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    async def is_available(self) -> bool:
        """Check if Ollama is available and a model can respond"""
        try:
            session = await self._get_session()
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.small_model,
                    "messages": [{"role": "user", "content": "hi"}],
                    "stream": False,
                    "options": {"num_predict": 1}
                },
                timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                return resp.status == 200
        except Exception:
            return False


ollama_client = OllamaClient()
