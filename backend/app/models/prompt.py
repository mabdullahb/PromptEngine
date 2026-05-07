from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base_class import Base

class Prompt(Base):
    __tablename__ = "prompts"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=True)
    
    original_text = Column(Text, nullable=False)
    enhanced_text = Column(Text, nullable=True)
    
    framework_used = Column(String, nullable=True)
    category = Column(String, nullable=True)
    
    # Store the structured data from the enhancement process
    metadata_json = Column(JSONB, nullable=True)

    # Relationships
    user = relationship("User", back_populates="prompts")
    workspace = relationship("Workspace", back_populates="prompts")

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    is_public = Column(Boolean, default=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
