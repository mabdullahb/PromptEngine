from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class EnhancePromptRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=5, description="The raw prompt to be enhanced.")
    provider_override: Optional[str] = Field(None, description="Optional override for the execution provider.")

class ClassificationMetadata(BaseModel):
    intent: Dict[str, Any]
    category: str

class EnhancementMetadata(BaseModel):
    category: str
    framework: str
    intent: Dict[str, Any]
    target_provider: str
    rewriting_provider: str
    timing_ms: Optional[float] = None
    estimated_tokens: Optional[int] = None

class EnhancePromptResponse(BaseModel):
    original_prompt: str
    enhanced_prompt: str
    metadata: EnhancementMetadata

class ClassifyPromptRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=5)

class ClassifyPromptResponse(BaseModel):
    raw_prompt: str
    classification: ClassificationMetadata
    recommended_provider: str

class FrameworkPreviewRequest(BaseModel):
    raw_prompt: str = Field(..., min_length=5)
    framework_name: str

class FrameworkPreviewResponse(BaseModel):
    framework_name: str
    system_prompt: str

class ProviderInfo(BaseModel):
    name: str
    description: str
    capabilities: List[str]

class PromptHistoryItem(BaseModel):
    id: int
    original_text: str
    enhanced_text: str
    framework_used: str
    category: str
    created_at: datetime
    metadata_json: Dict[str, Any]

class PromptHistoryResponse(BaseModel):
    items: List[PromptHistoryItem]
    total: int
