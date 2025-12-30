import httpx
import json
from .base import LLMProvider

class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.base_url = "http://localhost:11434"

    async def stream(self, prompt: str, system: str = None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json={"model": self.model, "messages": messages, "stream": True}
                ) as response:
                    if response.status_code != 200:
                        yield f"❌ Ollama Error: HTTP {response.status_code}"
                        return

                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if "message" in data:
                                    yield data["message"].get("content", "")
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield f"\n❌ Ollama Connection Error: {str(e)}"

    def models(self):
        return ["llama3.2", "phi3", "mistral", "nomic-embed-text"]
