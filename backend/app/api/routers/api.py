from app.api.routers import auth, engine, billing, usage

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(engine.router, prefix="/engine", tags=["engine"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
