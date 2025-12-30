from abc import ABC, abstractmethod
from typing import AsyncIterator, List

class LLMProvider(ABC):
    """Base class for all LLM providers"""
    name: str = "base"
    
    @abstractmethod
    async def stream(self, prompt: str, system: str = None) -> AsyncIterator[str]:
        """Stream response tokens"""
        yield ""
    
    @abstractmethod
    def models(self) -> List[str]:
        """List available models"""
        return []
