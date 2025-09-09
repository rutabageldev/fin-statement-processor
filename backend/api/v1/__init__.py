"""API v1 package."""

from fastapi import APIRouter

from .endpoints import admin_secrets
from .endpoints import institutions


api_router = APIRouter()
api_router.include_router(
    institutions.router, prefix="/institutions", tags=["institutions"]
)
api_router.include_router(admin_secrets.router, tags=["Admin - Secrets"])
