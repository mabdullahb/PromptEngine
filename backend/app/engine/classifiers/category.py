import json
from typing import Dict, Any, List
from app.engine.providers.factory import ProviderFactory

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

class CategoryClassifier:
    def __init__(self, provider_name: str = "groq"):
        # We default to Groq (Llama-3) for fast, cheap classification
        self.provider = ProviderFactory.get_provider(provider_name)
    
    async def classify(self, prompt: str) -> str:
        """
        Classifies the raw prompt into one of the predefined categories.
        """
        system_prompt = f"""
        You are an expert prompt classifier. Your job is to classify the user's prompt into EXACTLY ONE of the following categories:
        {json.dumps(CATEGORIES)}
        
        Respond ONLY with a JSON object containing a single key "category" with the classified category string.
        Do not add any additional text, markdown formatting, or explanation.
        """
        
        try:
            # We enforce JSON object return if the provider supports it.
            # Groq and OpenAI support this via response_format.
            response = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                response_format={"type": "json_object"},
                max_tokens=50
            )
            
            content = response["content"]
            # Fast parsing
            data = json.loads(content)
            category = data.get("category", "other").lower()
            
            # Fallback mapping if model hallucinates slightly
            if category not in [c.lower() for c in CATEGORIES]:
                return "other"
                
            return category
            
        except Exception as e:
            # Fallback in case of parsing or API error
            print(f"Classification error: {e}")
            return "other"
