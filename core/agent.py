from core.providers import gemini, ollama, openrouter
from .files import FileManager

# Registry
PROVIDERS = {
    "gemini": gemini.GeminiProvider,
    "ollama": ollama.OllamaProvider,
    "openrouter": openrouter.OpenRouterProvider,
    # Re-using OpenRouter class for specific aliases if preferred
    "mistral": openrouter.OpenRouterProvider,
    "huggingface": openrouter.OpenRouterProvider,
}


class NeuroAgent:
    def __init__(self, provider_name="ollama", **kwargs):
        self.provider_name = provider_name
        self.kwargs = kwargs
        self.files = FileManager()
        self._load_provider()

    def _load_provider(self):
        if self.provider_name not in PROVIDERS:
            raise ValueError(f"Provider {self.provider_name} not found.")

        provider_class = PROVIDERS[self.provider_name]
        self.provider = provider_class(**self.kwargs)

    async def stream(self, prompt):
        async for token in self.provider.stream(prompt):
            yield token

    def switch_provider(self, name, model=None):
        self.provider_name = name
        if model:
            self.kwargs["model"] = model
        self._load_provider()
        return f"Switched to {name} ({self.kwargs.get('model', 'default')})"
