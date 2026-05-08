from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class StructuredFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "Structured Formatting"
        
    @property
    def description(self) -> str:
        return "Enforces a strict output schema (JSON/XML) for programmatic consumption."

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        score = 0.1
        fmt = intent_data.get("desired_format", "").lower()
        
        # Super high score if format explicitly requests JSON, XML, YAML, schema, etc.
        if "json" in fmt or "xml" in fmt or "yaml" in fmt or "schema" in fmt:
            score += 0.8
            
        if category in ["ERP generation", "automation"]:
            score += 0.3
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        fmt = intent_data.get("desired_format", "JSON")
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer specializing in programmatic AI integrations.
        Rewrite the user's raw prompt using the Structured Formatting technique to ensure the LLM outputs valid {fmt}.
        
        Structured Formatting Strategy:
        1. Define the exact schema the AI must adhere to (infer it from the user's request if not explicitly provided).
        2. Explicitly instruct the AI to output ONLY valid {fmt} and no conversational filler.
        3. Clarify edge cases (e.g., what to do with missing fields).
        
        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}
        Desired Format: {fmt}

        Instructions:
        - Design a robust prompt that guarantees structured output.
        - Include an example of the desired schema in the prompt if helpful.
        - Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting.
        """
