from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=True)
    
    provider = Column(String, nullable=False) # e.g., 'openai', 'groq', 'gemini'
    model = Column(String, nullable=False) # e.g., 'gpt-4o', 'llama-3'
    
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="api_usage_logs")
