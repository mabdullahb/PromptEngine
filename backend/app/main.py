from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

from app.core.config import settings
from app.core.logging import setup_logging, logger

import sentry_sdk

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Advanced Prompt Engineering SaaS API",
    version="0.1.0",
)

# Tracing Middleware
class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response

from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Security Hardening
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.promptengine.ai"]
)

class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;"
        return response

app.add_middleware(SecureHeadersMiddleware)
app.add_middleware(TracingMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)

from app.api.middleware.rate_limit import RateLimitMiddleware
app.add_middleware(RateLimitMiddleware)

# Set CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from app.api.routers.api import api_router

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}

app.include_router(api_router, prefix=settings.API_V1_STR)
