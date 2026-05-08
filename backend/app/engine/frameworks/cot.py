from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class CoTFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "Chain-of-Thought (CoT)"
        
    @property
    def description(self) -> str:
        return "Forces the AI to reason step-by-step before providing an answer."

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        score = 0.2
        constraints_str = " ".join(intent_data.get("implicit_constraints", [])).lower()
        core_obj = intent_data.get("core_objective", "").lower()
        
        # CoT is vital for reasoning, math, logic, and deep research
        if category in ["research", "coding", "business"]:
            score += 0.4
            
        if "step" in constraints_str or "reason" in constraints_str or "analyze" in core_obj or "math" in core_obj or "logic" in core_obj:
            score += 0.4
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer. Rewrite the user's raw prompt using the Chain-of-Thought (CoT) prompting technique.
        
        Chain-of-Thought Strategy:
        1. Explicitly instruct the AI to "think step-by-step".
        2. Ask the AI to first output its reasoning process (e.g., inside <thinking> tags).
        3. Only after the reasoning is complete, ask it to output the final answer.
        
        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}

        Instructions:
        - Integrate the user's requirements into a prompt that demands step-by-step analytical reasoning before a conclusion.
        - Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting.
        """
