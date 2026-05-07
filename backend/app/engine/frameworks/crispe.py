from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class CrispeFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "CRISPE"
        
    @property
    def description(self) -> str:
        return "Capacity, Role, Insight, Statement, Personality, Experiment"

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer. Your task is to rewrite the user's raw prompt using the CRISPE framework to make it highly effective for complex reasoning tasks.
        
        CRISPE Framework:
        - C & R (Capacity & Role): What role should the AI act as?
        - I (Insight): Background context and information.
        - S (Statement): What you are asking the AI to do.
        - P (Personality): The style, tone, or personality of the response.
        - E (Experiment): Provide multiple options or variations in the output.

        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}

        Instructions:
        1. Analyze the raw prompt and fill out each element of the CRISPE framework explicitly.
        2. Combine these elements into a single, comprehensive, and highly optimized prompt ready to be sent to an AI.
        3. Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting for readability.
        """
