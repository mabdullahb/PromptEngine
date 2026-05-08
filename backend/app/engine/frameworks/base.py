from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFramework(ABC):
    """
    Abstract base class for all Prompt Engineering Frameworks.
    Implements the Strategy Pattern.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the framework (e.g., 'COSTAR')"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of what the framework does."""
        pass

    @abstractmethod
    def build_system_prompt(self, raw_prompt: str, intent_data: Dict[str, Any], category: str) -> str:
        """
        Builds the system instruction that will be sent to the LLM to perform the enhancement.
        """
        pass
        
    @abstractmethod
    def score(self, category: str, intent_data: Dict[str, Any]) -> float:
        """
        Calculates a score (0.0 to 1.0) indicating how well this framework suits the prompt.
        Higher score means better fit.
        """
        pass
        
    def format_output(self, enhanced_text: str) -> str:
        """
        Optional post-processing formatting for the enhanced prompt.
        """
        return enhanced_text.strip()
