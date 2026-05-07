import google.generativeai as genai
from typing import Dict, Any, Optional
from app.core.config import settings
from app.engine.providers.base import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.default_model = "gemini-1.5-pro-latest"
        self.provider_name = "gemini"

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
        
        # Configure model parameters
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        if response_format and response_format.get("type") == "json_object":
            generation_config.response_mime_type = "application/json"

        generative_model = genai.GenerativeModel(
            model_name=target_model,
            system_instruction=system_prompt,
            generation_config=generation_config
        )

        # Async generation
        response = await generative_model.generate_content_async(prompt)
        
        # Note: Gemini SDK usage metadata can be approximate or different structured
        prompt_token_count = generative_model.count_tokens(prompt).total_tokens
        completion_token_count = generative_model.count_tokens(response.text).total_tokens if response.text else 0

        return {
            "content": response.text,
            "usage": {
                "prompt_tokens": prompt_token_count,
                "completion_tokens": completion_token_count,
                "total_tokens": prompt_token_count + completion_token_count
            },
            "model": target_model,
            "provider": self.provider_name
        }
