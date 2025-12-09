from app.routers.auth_router import router as auth_router
from app.routers.config_router import router as config_router
from app.routers.analysis_router import router as analysis_router

__all__ = ["auth_router", "config_router", "analysis_router"]
