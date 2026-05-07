from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.api_usage import ApiUsageLog
from app.models.prompt import Prompt
from app.schemas.prompt import EnhancePromptRequest, EnhancePromptResponse
from app.engine.enhancers.pipeline import EnhancementPipeline

router = APIRouter()
pipeline = EnhancementPipeline()

@router.post("/enhance", response_model=EnhancePromptResponse)
async def enhance_prompt(
    request: EnhancePromptRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Takes a raw user prompt, classifies it, selects a framework, and enhances it.
    Requires authentication. Tracks API usage.
    """
    try:
        # Run the enhancement pipeline
        result = await pipeline.enhance(
            raw_prompt=request.raw_prompt,
            target_provider=request.target_provider,
            target_model=request.target_model
        )
        
        # Log the API usage in the database for billing/limits
        usage_data = result["metadata"]["usage"]
        usage_log = ApiUsageLog(
            user_id=current_user.id,
            provider=result["metadata"]["provider_used"],
            model=request.target_model or "default",
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0)
        )
        
        # Save the prompt history
        prompt_record = Prompt(
            user_id=current_user.id,
            original_text=result["original_prompt"],
            enhanced_text=result["enhanced_prompt"],
            framework_used=result["metadata"]["framework"],
            category=result["metadata"]["category"],
            metadata_json=result["metadata"]["intent"]
        )
        
        db.add(usage_log)
        db.add(prompt_record)
        
        # Tie the usage log to the prompt for analytical tracking
        await db.commit()
        await db.refresh(prompt_record)
        
        usage_log.prompt_id = prompt_record.id
        await db.commit()

        return EnhancePromptResponse(**result)

    except Exception as e:
        # In a real app, log the detailed exception, return a generic error to client
        print(f"Enhancement Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during prompt enhancement.")
