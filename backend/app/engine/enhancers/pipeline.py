from typing import Dict, Any, Optional
from app.engine.classifiers.intent import IntentDetector
from app.engine.classifiers.category import CategoryClassifier
from app.engine.frameworks.factory import FrameworkFactory
from app.engine.providers.factory import ProviderFactory

class EnhancementPipeline:
    def __init__(self):
        # Initialize core components
        self.intent_detector = IntentDetector()
        self.category_classifier = CategoryClassifier()

    async def enhance(
        self, 
        raw_prompt: str, 
        target_provider: str = "openai",
        target_model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates the full Prompt Enhancement Pipeline:
        1. Detect Intent
        2. Classify Category
        3. Select Framework
        4. Generate Enhanced Prompt via Target Provider
        5. Return structured output
        """
        
        # 1. & 2. Parallel Classification (for speed)
        # Note: In a real high-throughput system, you'd use asyncio.gather here
        # For simplicity and clear logic progression, we await sequentially.
        
        intent_data = await self.intent_detector.detect(raw_prompt)
        category = await self.category_classifier.classify(raw_prompt)
        
        # 3. Select Framework based on classification
        framework = FrameworkFactory.select_optimal_framework(category, intent_data)
        
        # 4. Generate System Prompt
        system_prompt = framework.build_system_prompt(raw_prompt, intent_data, category)
        
        # 5. Call Target Provider to execute the enhancement
        provider = ProviderFactory.get_provider(target_provider)
        
        response = await provider.generate_completion(
            prompt="Optimize the raw prompt exactly as instructed by the framework.",
            system_prompt=system_prompt,
            model=target_model,
            temperature=0.4, # Lower temperature for more deterministic, structured rewriting
        )
        
        raw_enhanced_text = response.get("content", "")
        
        # 6. Format and finalize output
        enhanced_prompt = framework.format_output(raw_enhanced_text)
        
        return {
            "original_prompt": raw_prompt,
            "enhanced_prompt": enhanced_prompt,
            "metadata": {
                "category": category,
                "framework": framework.name,
                "intent": intent_data,
                "provider_used": target_provider,
                "usage": response.get("usage", {})
            }
        }
