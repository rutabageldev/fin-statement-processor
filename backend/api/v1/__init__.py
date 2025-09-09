"""API v1 package."""

from fastapi import APIRouter

from .endpoints import institutions


api_router = APIRouter()
api_router.include_router(
    institutions.router, prefix="/institutions", tags=["institutions"]
)
