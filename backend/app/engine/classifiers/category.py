import json
from typing import Optional
from app.core.logging import logger
from app.engine.classifiers.base import BaseClassifier

CATEGORIES = [
    "coding",
    "marketing",
    "business",
    "ERP generation",
    "image generation",
    "research",
    "content writing",
    "automation",
    "other"
]

class CategoryClassifier(BaseClassifier):
    def __init__(self, default_provider: str = "groq"):
        # We default to Groq (Llama-3) for fast, cheap classification
        super().__init__(default_provider=default_provider)
    
    async def classify(self, prompt: str, provider_override: Optional[str] = None) -> str:
        """
        Classifies the raw prompt into one of the predefined categories.
        """
        system_prompt = f"""
        You are an expert prompt classifier. Your job is to classify the user's prompt into EXACTLY ONE of the following categories:
        {json.dumps(CATEGORIES)}
        
        Respond ONLY with a JSON object containing a single key "category" with the classified category string.
        Do not add any additional text, markdown formatting, or explanation.
        """
        
        provider = self._get_provider(provider_override)
        
        try:
            response = await provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                response_format={"type": "json_object"},
                max_tokens=50
            )
            
            content = response["content"]
            data = json.loads(content)
            category = data.get("category", "other").lower()
            
            # Fallback mapping if model hallucinates slightly
            if category not in [c.lower() for c in CATEGORIES]:
                return "other"
                
            return category
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from category classifier: {e}")
        except Exception as e:
            logger.error(f"Classification error: {e}")
            
        return "other"
