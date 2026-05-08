import redis.asyncio as redis
from typing import Tuple
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.subscription import PlanType
from app.core.logging import logger

class QuotaService:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        
    def _get_daily_key(self, user_id: str) -> str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        return f"quota:{user_id}:{date_str}"

    def get_limit(self, plan: PlanType) -> int:
        limits = {
            PlanType.FREE: 10,
            PlanType.PRO: 1000,
            PlanType.TEAM: 1000000 # Effectively unlimited
        }
        return limits.get(plan, 10)

    async def check_quota(self, user_id: str, plan: PlanType) -> Tuple[bool, int, int]:
        """
        Checks if user has enough quota left.
        Returns (allowed, current_usage, limit)
        """
        key = self._get_daily_key(user_id)
        limit = self.get_limit(plan)
        
        usage = await self.redis.get(key)
        current_usage = int(usage) if usage else 0
        
        if current_usage >= limit:
            return False, current_usage, limit
            
        return True, current_usage, limit

    async def increment_usage(self, user_id: str):
        """Increments the daily usage counter."""
        key = self._get_daily_key(user_id)
        await self.redis.incr(key)
        # Set expiry to 25 hours to ensure it clears after the day ends
        await self.redis.expire(key, 25 * 3600)
        
    async def get_usage_summary(self, user_id: str, plan: PlanType) -> dict:
        key = self._get_daily_key(user_id)
        limit = self.get_limit(plan)
        usage = await self.redis.get(key)
        current_usage = int(usage) if usage else 0
        
        return {
            "usage": current_usage,
            "limit": limit,
            "remaining": max(0, limit - current_usage),
            "reset_in_seconds": self._seconds_until_midnight()
        }

    def _seconds_until_midnight(self) -> int:
        now = datetime.utcnow()
        tomorrow = now.date() + timedelta(days=1)
        midnight = datetime.combine(tomorrow, datetime.min.time())
        return int((midnight - now).total_seconds())

quota_service = QuotaService()
