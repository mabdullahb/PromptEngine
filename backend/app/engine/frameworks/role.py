from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class RoleFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "Role Prompting"
        
    @property
    def description(self) -> str:
        return "Assigns a specific persona or expert role to the AI."

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        # High score if the constraints or prompt strongly imply a persona
        score = 0.4
        constraints_str = " ".join(intent_data.get("implicit_constraints", [])).lower()
        core_obj = intent_data.get("core_objective", "").lower()
        
        if "act as" in core_obj or "persona" in constraints_str or "expert" in constraints_str:
            score += 0.5
            
        if category in ["business", "marketing", "content writing"]:
            score += 0.1
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        
        return f"""
        You are an expert Prompt Engineer. Rewrite the user's raw prompt using the Role Prompting technique.
        
        Role Prompting Strategy:
        1. Identify the most suitable expert persona for the task.
        2. Set the persona clearly at the beginning of the prompt (e.g., "Act as an expert [Role]").
        3. Define the task from the perspective of that persona.
        
        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}

        Instructions:
        - Determine the optimal role/persona.
        - Write a highly optimized prompt that commands the AI to adopt this role.
        - Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting.
        """
