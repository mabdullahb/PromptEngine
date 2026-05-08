import json
from typing import Dict, Any, Optional
from app.core.logging import logger
from app.engine.classifiers.base import BaseClassifier

class IntentDetector(BaseClassifier):
    def __init__(self, default_provider: str = "groq"):
        super().__init__(default_provider=default_provider)
    
    async def classify(self, prompt: str, provider_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyzes the prompt to extract the core intent, desired format, and implicit constraints.
        """
        system_prompt = """
        You are an expert NLP intent detector for a prompt engineering pipeline.
        Analyze the user's raw prompt and extract the following:
        1. "core_objective": A concise summary of what the user is trying to achieve.
        2. "desired_format": The requested output format (e.g., table, code, essay, json). If none is specified, return "unspecified".
        3. "implicit_constraints": A list of constraints implied by the prompt (e.g., tone, length, specific tools).
        
        Respond ONLY with a JSON object containing these three keys.
        """
        
        provider = self._get_provider(provider_override)
        
        try:
            response = await provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                response_format={"type": "json_object"},
                max_tokens=250
            )
            
            content = response["content"]
            data = json.loads(content)
            
            return {
                "core_objective": data.get("core_objective", "Unknown objective"),
                "desired_format": data.get("desired_format", "unspecified"),
                "implicit_constraints": data.get("implicit_constraints", [])
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from intent detector: {e}")
        except Exception as e:
            logger.error(f"Intent detection error: {e}")
            
        return {
            "core_objective": "Determine the user's intent",
            "desired_format": "unspecified",
            "implicit_constraints": []
        }
