from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAIProvider(ABC):
    """
    Abstract base class for AI Providers.
    Ensures that all integrations (OpenAI, Groq, Gemini) follow a unified interface.
    """
    
    @abstractmethod
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a text completion.
        
        Returns:
            Dict containing:
                - 'content': The generated text string
                - 'usage': Dict with 'prompt_tokens', 'completion_tokens', 'total_tokens'
                - 'model': The actual model used
                - 'provider': The provider name string
        """
        pass
