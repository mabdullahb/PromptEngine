from pydantic import BaseModel
from typing import Optional, Dict, Any

class EnhancePromptRequest(BaseModel):
    raw_prompt: str
    target_provider: Optional[str] = "openai"
    target_model: Optional[str] = None

class EnhancePromptResponse(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    metadata: Dict[str, Any]
