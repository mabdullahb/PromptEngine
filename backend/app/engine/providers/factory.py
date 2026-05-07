from typing import Optional
from fastapi import HTTPException
from app.engine.providers.base import BaseAIProvider
from app.engine.providers.openai_provider import OpenAIProvider
from app.engine.providers.groq_provider import GroqProvider
from app.engine.providers.gemini_provider import GeminiProvider
from app.engine.providers.openrouter_provider import OpenRouterProvider

class ProviderFactory:
    _providers = {}

    @classmethod
    def get_provider(cls, provider_name: str) -> BaseAIProvider:
        """
        Singleton-like factory method to return the requested AI Provider.
        Instantiates it on the first call and caches it.
        """
        provider_name = provider_name.lower()
        if provider_name in cls._providers:
            return cls._providers[provider_name]

        if provider_name == "openai":
            provider = OpenAIProvider()
        elif provider_name == "groq":
            provider = GroqProvider()
        elif provider_name == "gemini":
            provider = GeminiProvider()
        elif provider_name == "openrouter":
            provider = OpenRouterProvider()
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {provider_name}")

        cls._providers[provider_name] = provider
        return provider
