import json
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache Get Error: {e}")
            return None

    async def set(self, key: str, value: Any, expire: int = 3600):
        try:
            await self.redis.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            logger.error(f"Cache Set Error: {e}")

    async def delete(self, key: str):
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.error(f"Cache Delete Error: {e}")

cache = CacheManager()
