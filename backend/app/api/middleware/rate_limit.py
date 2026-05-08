import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis
from app.core.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    async def dispatch(self, request: Request, call_next):
        # We only rate limit API routes
        if not request.url.path.startswith(settings.API_V1_STR):
            return await call_next(request)

        # Skip rate limiting for auth routes
        if "/auth/" in request.url.path:
            return await call_next(request)

        # Get user ID from state (set by Auth middleware later or using IP for now)
        # Ideally, we'd want to rate limit AFTER auth, but middleware runs in order
        # For simplicity in this step, let's use IP if no user is found
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}:{request.url.path}"
        
        # Simple sliding window rate limiting (e.g., 60 requests per minute per IP/route)
        current_time = int(time.time())
        window = 60
        limit = 60
        
        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.zremrangebyscore(key, 0, current_time - window)
            await pipe.zadd(key, {str(current_time): current_time})
            await pipe.zcard(key)
            await pipe.expire(key, window)
            _, _, count, _ = await pipe.execute()

        if count > limit:
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        response = await call_next(request)
        return response
