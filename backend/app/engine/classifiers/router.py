from typing import Dict, Any

class ProviderRouter:
    """
    Determines the optimal AI provider based on intent and category classification.
    """
    
    # Simple rule-based routing for Phase 4
    # Future enhancement: Load from database/workspace settings
    ROUTING_RULES = {
        "coding": "openrouter",      # Best for complex coding (Claude 3 / GPT-4)
        "research": "openai",        # Good for deep research (GPT-4)
        "content writing": "openai", # Good for creative writing
        "business": "openai",        # Good for business logic
        "ERP generation": "openrouter", # Complex struct gen
        "marketing": "groq",         # Fast, Llama-3 is usually sufficient
        "automation": "openrouter",  # Needs high reasoning
        "other": "groq",             # Default fast fallback
        "image generation": "openai" # Not directly a text model, but routing to an OpenAI DALL-E integration later
    }

    def route(self, classification_data: Dict[str, Any]) -> str:
        """
        Takes the aggregated output from all classifiers and returns the recommended provider name.
        """
        category = classification_data.get("category", "other")
        
        # In a more advanced version, we could use intent data here:
        # e.g., if intent["desired_format"] == "json", ensure we use a provider that supports json mode.
        # For now, we rely primarily on category rules.
        
        provider = self.ROUTING_RULES.get(category, "groq")
        return provider
