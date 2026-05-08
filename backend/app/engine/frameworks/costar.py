from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class CostarFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "COSTAR"
        
    @property
    def description(self) -> str:
        return "Context, Objective, Style, Tone, Audience, Response"

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        # COSTAR is a great general-purpose framework
        score = 0.5
        
        # Particularly good when style/tone/audience are explicitly mentioned
        constraints_str = " ".join(intent_data.get("implicit_constraints", [])).lower()
        if "tone" in constraints_str or "style" in constraints_str or "audience" in constraints_str:
            score += 0.3
            
        if category in ["marketing", "content writing", "business"]:
            score += 0.2
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer. Your task is to rewrite the user's raw prompt using the COSTAR framework to make it highly effective.
        
        COSTAR Framework:
        - C (Context): Provide background information.
        - O (Objective): Define the clear task.
        - S (Style): Specify the writing style.
        - T (Tone): Set the attitude.
        - A (Audience): Identify who the response is for.
        - R (Response): Define the format.

        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}
        Desired Format: {intent_data.get('desired_format')}

        Instructions:
        1. Analyze the raw prompt and fill out each element of the COSTAR framework explicitly.
        2. Combine these elements into a single, comprehensive, and highly optimized prompt ready to be sent to an AI.
        3. Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting for readability.
        """
