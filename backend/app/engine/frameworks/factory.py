from typing import Dict, Type
from app.engine.frameworks.base import BaseFramework
from app.engine.frameworks.costar import CostarFramework
from app.engine.frameworks.crispe import CrispeFramework

class FrameworkFactory:
    _frameworks: Dict[str, BaseFramework] = {
        "costar": CostarFramework(),
        "crispe": CrispeFramework(),
    }

    @classmethod
    def get_framework(cls, name: str) -> BaseFramework:
        """Returns the specific framework implementation by name."""
        name = name.lower()
        if name in cls._frameworks:
            return cls._frameworks[name]
        # Default to COSTAR if unknown
        return cls._frameworks["costar"]

    @classmethod
    def select_optimal_framework(cls, category: str, intent_data: dict) -> BaseFramework:
        """
        Strategy selector: dynamically chooses the best framework based on category and intent.
        """
        # Complex reasoning, research, or content writing benefits from CRISPE
        if category in ["research", "content writing", "business"] or "experiment" in intent_data.get("implicit_constraints", []):
            return cls.get_framework("crispe")
        
        # General formatting, coding, marketing, automation default to COSTAR
        return cls.get_framework("costar")
