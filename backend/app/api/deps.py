from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
import redis.asyncio as redis

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.schemas.token import TokenPayload
from app.services.user_service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_db() -> Generator:
    async with AsyncSessionLocal() as session:
        yield session

async def get_redis() -> Generator:
    redis_client = redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf-8", decode_responses=True)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()

async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    token: str = Depends(oauth2_scheme),
    redis_client: redis.Redis = Depends(get_redis)
) -> User:
    try:
        # Check if token is blocklisted
        is_blocklisted = await redis_client.get(f"blocklist:{token}")
        if is_blocklisted:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if token_data.type != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
            
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        
    user = await get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user

from app.models.subscription import PlanType, SubscriptionStatus, Subscription

async def get_current_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Subscription:
    # We use join to fetch the subscription
    from sqlalchemy import select
    query = select(Subscription).where(Subscription.user_id == current_user.id)
    result = await db.execute(query)
    subscription = result.scalar_one_none()
    
    if not subscription:
        # Create a default free subscription if missing
        subscription = Subscription(user_id=current_user.id, plan_type=PlanType.FREE, status=SubscriptionStatus.ACTIVE)
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        
    return subscription

class CheckPlan:
    def __init__(self, required_plan: PlanType):
        self.required_plan = required_plan

    def __call__(
        self, 
        subscription: Subscription = Depends(get_current_subscription)
    ) -> bool:
        # FREE < PRO < TEAM
        plan_weights = {
            PlanType.FREE: 0,
            PlanType.PRO: 1,
            PlanType.TEAM: 2
        }
        
        if plan_weights.get(subscription.plan_type) < plan_weights.get(self.required_plan):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"This feature requires a {self.required_plan.value.capitalize()} subscription."
            )
        return True
