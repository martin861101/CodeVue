import httpx
from .base import LLMProvider

class OllamaProvider(LLMProvider):
    name = "ollama"
    
    def __init__(self, model: str = "llama3"):
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
                    async for line in response.aiter_lines():
                        if line.strip():
                            import json
                            data = json.loads(line)
                            if "message" in data:
                                yield data["message"].get("content", "")
        except Exception as e:
            yield f"\n❌ Ollama error: {str(e)}"
    
    def models(self):
        return ["llama3", "mistral", "codellama", "phi3", "qwen2.5-coder"]
