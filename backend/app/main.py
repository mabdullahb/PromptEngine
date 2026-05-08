from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Advanced Prompt Engineering SaaS API",
    version="0.1.0",
)

from app.api.middleware.rate_limit import RateLimitMiddleware

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(RateLimitMiddleware)

from app.api.routers.api import api_router

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(api_router, prefix=settings.API_V1_STR)
