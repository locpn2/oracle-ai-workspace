from typing import List, Optional, Dict, Any
import aiohttp
from ..core.config import get_settings

settings = get_settings()


class OllamaClient:
    """Client for Ollama API"""
    
    def __init__(self, base_url: str = None, model: str = "llama3.2", 
                 embed_model: str = "nomic-embed-text"):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model
        self.embed_model = embed_model
    
    async def generate(self, prompt: str, system: str = None, 
                       temperature: float = 0.3, max_tokens: int = 500) -> str:
        """Generate text using /api/generate endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
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
                    timeout=aiohttp.ClientTimeout(total=60)
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
                   temperature: float = 0.3) -> str:
        """Generate using chat endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature
                    }
                }
                
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
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
            async with aiohttp.ClientSession() as session:
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
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return [m.get("name") for m in result.get("models", [])]
                    return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    async def is_available(self) -> bool:
        """Check if Ollama is available"""
        try:
            models = await self.list_models()
            return True
        except:
            return False


ollama_client = OllamaClient()