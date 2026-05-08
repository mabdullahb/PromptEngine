from typing import Dict, Any
from app.engine.frameworks.base import BaseFramework
from app.engine.frameworks.costar import CostarFramework
from app.engine.frameworks.crispe import CrispeFramework
from app.engine.frameworks.rtf import RTFFramework
from app.engine.frameworks.role import RoleFramework
from app.engine.frameworks.few_shot import FewShotFramework
from app.engine.frameworks.cot import CoTFramework
from app.engine.frameworks.structured import StructuredFramework
from app.core.logging import logger

class FrameworkFactory:
    _frameworks: Dict[str, BaseFramework] = {
        "costar": CostarFramework(),
        "crispe": CrispeFramework(),
        "rtf": RTFFramework(),
        "role": RoleFramework(),
        "few_shot": FewShotFramework(),
        "cot": CoTFramework(),
        "structured": StructuredFramework()
    }

    @classmethod
    def get_framework(cls, name: str) -> BaseFramework:
        """Returns the specific framework implementation by name."""
        name = name.lower()
        if name in cls._frameworks:
            return cls._frameworks[name]
        return cls._frameworks["costar"]

    @classmethod
    def select_optimal_framework(cls, category: str, intent_data: Dict[str, Any]) -> BaseFramework:
        """
        Strategy selector: dynamically chooses the best framework based on category and intent
        by calling the score() method of each registered framework.
        """
        best_framework = None
        highest_score = -1.0

        for name, framework in cls._frameworks.items():
            try:
                score = framework.score(category, intent_data)
                logger.info(f"Framework '{name}' scored {score} for category '{category}'")
                
                if score > highest_score:
                    highest_score = score
                    best_framework = framework
            except Exception as e:
                logger.error(f"Error scoring framework {name}: {e}")

        if not best_framework:
            logger.warning("No framework scored higher than -1. Defaulting to COSTAR.")
            best_framework = cls._frameworks["costar"]

        logger.info(f"Selected optimal framework: {best_framework.name}")
        return best_framework
