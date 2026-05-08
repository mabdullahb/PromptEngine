from typing import Dict, Any, Optional
from app.engine.classifiers.engine import ClassificationEngine
from app.engine.frameworks.factory import FrameworkFactory
from app.engine.providers.factory import ProviderFactory
from app.core.logging import logger

class EnhancementPipeline:
    def __init__(self):
        # Initialize core orchestrator
        self.classification_engine = ClassificationEngine()

    async def enhance(
        self, 
        raw_prompt: str, 
        provider_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates the full Prompt Enhancement Pipeline:
        1. Classify Prompt (Intent & Category) and Route
        2. Select Optimal Framework
        3. Generate Enhanced Prompt via robust Rewriting Provider
        4. Apply Target Provider Optimizations
        5. Return structured output
        """
        logger.info("Starting enhancement pipeline")
        
        # 1. Classification & Routing
        classification_result = await self.classification_engine.analyze_and_route(
            prompt=raw_prompt, 
            provider_override=provider_override
        )
        
        intent_data = classification_result["classification"]["intent"]
        category = classification_result["classification"]["category"]
        
        # Determine the final execution provider. 
        # If user didn't override, use the engine's recommended provider.
        target_provider = provider_override or classification_result["recommended_provider"]
        
        # 2. Select Framework based on classification
        framework = FrameworkFactory.select_optimal_framework(category, intent_data)
        
        # 3. Generate System Prompt using the selected framework
        system_prompt = framework.build_system_prompt(raw_prompt, intent_data, category)
        
        # 4. Call Rewriting Provider to execute the enhancement
        # We use a highly capable model for rewriting, defaulting to openai for stability,
        # but could be customized in future.
        rewriting_provider = ProviderFactory.get_provider("openai")
        
        try:
            logger.info(f"Generating enhancement using {framework.name} framework")
            response = await rewriting_provider.generate_completion(
                prompt="Optimize the raw prompt exactly as instructed by the framework. Return ONLY the optimized string.",
                system_prompt=system_prompt,
                temperature=0.3, # Low temp for deterministic rewriting
            )
            raw_enhanced_text = response.get("content", "").strip()
        except Exception as e:
            logger.error(f"Failed to generate enhancement: {e}")
            raw_enhanced_text = raw_prompt # Fallback to original prompt
            
        # 5. Format and apply Target Provider Optimizations
        enhanced_prompt = framework.format_output(raw_enhanced_text)
        
        # Provider-Aware Optimization:
        # e.g., Anthropic models (often via OpenRouter) perform best with <system> and <user> XML tags
        if "openrouter" in target_provider.lower() and "claude" in str(intent_data).lower():
            # Basic example of provider-aware wrapping
            enhanced_prompt = f"<prompt>\n{enhanced_prompt}\n</prompt>"

        return {
            "original_prompt": raw_prompt,
            "enhanced_prompt": enhanced_prompt,
            "metadata": {
                "category": category,
                "framework": framework.name,
                "intent": intent_data,
                "target_provider": target_provider,
                "rewriting_provider": "openai"
            }
        }
