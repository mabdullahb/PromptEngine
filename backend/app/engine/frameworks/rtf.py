from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework

class RTFFramework(BaseFramework):
    @property
    def name(self) -> str:
        return "RTF"
        
    @property
    def description(self) -> str:
        return "Role, Task, Format"

    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        # RTF is great for simple instructions where format is important
        score = 0.5 # Baseline
        
        if intent_data.get("desired_format") not in ["unspecified", "text"]:
            score += 0.3
            
        if category in ["content writing", "marketing"]:
            score += 0.1
            
        # If it requires heavy logic, RTF is too simple
        if category in ["coding", "research"]:
            score -= 0.2
            
        return min(max(score, 0.0), 1.0)

    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        constraints = ", ".join(intent_data.get("implicit_constraints", []))
        format_req = intent_data.get("desired_format", "clear and concise text")
        
        return f"""
        You are an expert Prompt Engineer. Rewrite the user's raw prompt using the RTF (Role, Task, Format) framework.
        
        RTF Framework:
        - Role: Define who the AI is.
        - Task: Define what the AI needs to do.
        - Format: Define how the output should be structured.

        User's Raw Prompt: "{raw_prompt}"
        Category: {category}
        Core Intent: {intent_data.get('core_objective')}
        Implicit Constraints: {constraints}
        Desired Format: {format_req}

        Instructions:
        1. Fill out each element of the RTF framework explicitly.
        2. Combine these elements into a single, comprehensive, and highly optimized prompt ready to be sent to an AI.
        3. Do not include introductory text. Return ONLY the final optimized prompt string. Ensure it uses markdown formatting.
        """
