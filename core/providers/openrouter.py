from openai import AsyncOpenAI
from .base import LLMProvider

class OpenRouterProvider(LLMProvider):
    name = "openrouter"
    
    def __init__(self, api_key: str, model: str = "meta-llama/llama-3.1-8b-instruct"):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
        self.messages = []
    
    async def stream(self, prompt: str, system: str = None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n❌ Error: {str(e)}"
    
    def models(self):
        return [
            "meta-llama/llama-3.1-8b-instruct",
            "meta-llama/llama-3.1-70b-instruct",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4-turbo"
        ]
