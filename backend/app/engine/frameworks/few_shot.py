from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class FewShotFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "Few-Shot"
        
    @property
    def description(self) -> str:
        return "Provides specific examples in the prompt to guide the LLM's output."

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        # Few-shot is excellent when format matters heavily or patterns are requested
        score = 0.3
        constraints_str = " ".join(intent_data.get("implicit_constraints", [])).lower()
        core_obj = intent_data.get("core_objective", "").lower()
        
        if "example" in constraints_str or "pattern" in constraints_str or "translate" in core_obj:
            score += 0.5
            
        if intent_data.get("desired_format") not in ["unspecified", "text"]:
            score += 0.2
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer. Rewrite the user's raw prompt using the Few-Shot Prompting technique.
        
        Few-Shot Prompting Strategy:
        1. Define the task clearly.
        2. Provide 2 to 3 high-quality examples of the Input and desired Output.
        3. End with the actual user's input to trigger the AI to continue the pattern.
        
        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}
        Desired Format: {intent_data.get('desired_format')}

        Instructions:
        - Generate realistic examples that perfectly fit the user's implicit constraints and format.
        - Combine the instructions, examples, and target request into one cohesive prompt.
        - Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting.
        """
