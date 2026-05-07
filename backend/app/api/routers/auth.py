from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.api.deps import get_db, get_redis, get_current_user
from app.services import user_service
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user = await user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_service.create_user(db, user_in=user_in)
    return user

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_service.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id, expires_delta=refresh_token_expires),
        "token_type": "bearer",
    }

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    token: str = Depends(get_current_user), # This is a placeholder logic
    redis_client: redis.Redis = Depends(get_redis)
) -> Any:
    """
    Logout the current user (blocklist the token).
    Note: Requires custom logic to extract raw token from request header in production.
    """
    # For a real blocklist, we'd extract the raw JWT token from the Authorization header 
    # and set it in Redis with an expiration equal to the token's remaining TTL.
    # await redis_client.setex(f"blocklist:{raw_token}", ttl, "true")
    return {"message": "Successfully logged out"}

@router.post("/google")
async def google_auth_placeholder() -> Any:
    """
    Placeholder for Google OAuth integration.
    Expects an id_token from the client, verifies it with Google, and returns a JWT.
    """
    # To be implemented: Validate Google id_token, get user email, 
    # create user if not exists, and return JWT token pair.
    return {"message": "Google Auth not fully implemented yet"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user.
    """
    return current_user
