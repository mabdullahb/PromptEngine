from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.api.deps import get_db, get_current_user, get_current_subscription
from app.models.user import User
from app.models.subscription import Subscription
from app.services.usage_service import usage_service
from app.services.quota_service import quota_service

router = APIRouter()

@router.get("/summary")
async def get_usage_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    subscription: Subscription = Depends(get_current_subscription)
) -> Any:
    """Get overall usage statistics and daily quota summary."""
    stats = await usage_service.get_user_stats(db, str(current_user.id))
    quota = await quota_service.get_usage_summary(str(current_user.id), subscription.plan_type)
    
    return {
        "stats": stats,
        "quota": quota,
        "plan": subscription.plan_type
    }
