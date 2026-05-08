from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as redis
from app.api.deps import get_db, get_redis
from app.core.logging import logger

router = APIRouter()

@router.get("/detailed")
async def detailed_health(
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    """
    Detailed health check for production monitoring.
    Verifies database and redis connectivity.
    """
    health_status = {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "version": "0.1.0"
    }
    
    try:
        # Check DB
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Health Check - DB Failure: {e}")
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"

    try:
        # Check Redis
        await redis_client.ping()
    except Exception as e:
        logger.error(f"Health Check - Redis Failure: {e}")
        health_status["redis"] = "disconnected"
        health_status["status"] = "unhealthy"

    return health_status
