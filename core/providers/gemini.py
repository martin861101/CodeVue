from google import genai
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def stream(self, prompt: str, system: str = None):
        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        try:
            response = self.client.models.generate_content_stream(
                model=self.model, contents=contents
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n❌ Gemini error: {str(e)}"

    def models(self):
        return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
