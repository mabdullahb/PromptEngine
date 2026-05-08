from abc import ABC, abstractmethod
from typing import Any, Optional
from app.engine.providers.factory import ProviderFactory
from app.core.logging import logger

class BaseClassifier(ABC):
    """
    Abstract base class for all prompt classifiers.
    """
    def __init__(self, default_provider: str = "groq"):
        self.default_provider = default_provider
        
    def _get_provider(self, provider_override: Optional[str] = None):
        """Helper to get the configured or overridden provider."""
        provider_name = provider_override or self.default_provider
        try:
            return ProviderFactory.get_provider(provider_name)
        except Exception as e:
            logger.error(f"Failed to load provider '{provider_name}': {e}")
            raise
        
    @abstractmethod
    async def classify(self, prompt: str, provider_override: Optional[str] = None) -> Any:
        """
        Analyze the prompt and return classification results.
        
        Args:
            prompt: The raw user prompt to classify.
            provider_override: Optional provider to use instead of the default.
            
        Returns:
            Classification results (varies by subclass).
        """
        pass
