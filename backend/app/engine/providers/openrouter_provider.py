import openai
from typing import Dict, Any, Optional
from app.core.config import settings
from app.engine.providers.base import BaseAIProvider

class OpenRouterProvider(BaseAIProvider):
    def __init__(self):
        # OpenRouter uses the OpenAI SDK with a custom base URL
        self.client = openai.AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.default_model = "anthropic/claude-3-haiku"
        self.provider_name = "openrouter"

    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        
        target_model = model or self.default_model
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            # OpenRouter headers for rankings and UI
            "extra_headers": {
                "HTTP-Referer": "https://promptengine.app", 
                "X-Title": "PromptEngine",
            }
        }
        
        if response_format:
            kwargs["response_format"] = response_format

        response = await self.client.chat.completions.create(**kwargs)
        
        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "model": target_model,
            "provider": self.provider_name
        }
