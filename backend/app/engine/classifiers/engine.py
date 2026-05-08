import asyncio
from typing import Dict, Any, Optional

from app.core.logging import logger
from app.engine.classifiers.intent import IntentDetector
from app.engine.classifiers.category import CategoryClassifier
from app.engine.classifiers.router import ProviderRouter

class ClassificationEngine:
    """
    Orchestrates the prompt classification pipeline.
    Runs multiple classifiers concurrently and determines the best AI provider for the prompt.
    """
    def __init__(self):
        # Instantiate available classifiers
        self.intent_detector = IntentDetector()
        self.category_classifier = CategoryClassifier()
        self.router = ProviderRouter()
        
    async def analyze_and_route(self, prompt: str, provider_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes the prompt by running all registered classifiers concurrently,
        then routes it to the optimal provider.
        
        Args:
            prompt: The raw user prompt.
            provider_override: Optional override for the classification provider (defaults to Groq).
            
        Returns:
            A dictionary containing the full classification payload and the recommended provider.
        """
        logger.info("Starting classification pipeline for prompt.")
        
        # Run classifiers concurrently to minimize latency
        intent_task = asyncio.create_task(
            self.intent_detector.classify(prompt, provider_override=provider_override)
        )
        category_task = asyncio.create_task(
            self.category_classifier.classify(prompt, provider_override=provider_override)
        )
        
        try:
            intent_result, category_result = await asyncio.gather(
                intent_task, category_task, return_exceptions=True
            )
        except Exception as e:
            logger.error(f"Unexpected error during concurrent classification: {e}")
            intent_result = {"core_objective": "Determine the user's intent", "desired_format": "unspecified", "implicit_constraints": []}
            category_result = "other"
            
        # Handle individual task exceptions if any
        if isinstance(intent_result, Exception):
            logger.error(f"Intent detection failed: {intent_result}")
            intent_result = {"core_objective": "Determine the user's intent", "desired_format": "unspecified", "implicit_constraints": []}
            
        if isinstance(category_result, Exception):
            logger.error(f"Category classification failed: {category_result}")
            category_result = "other"

        # Aggregate the results
        classification_data = {
            "intent": intent_result,
            "category": category_result
        }
        
        # Route to the best provider based on classification
        recommended_provider = self.router.route(classification_data)
        
        payload = {
            "classification": classification_data,
            "recommended_provider": recommended_provider
        }
        
        logger.info(f"Classification complete. Recommended provider: {recommended_provider}")
        return payload
