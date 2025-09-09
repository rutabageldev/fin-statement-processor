"""Institution endpoints for Ledgerly API."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database
from models.orm import Institution


router = APIRouter()


@router.get("/", response_model=list[dict[str, str | None]])
async def list_institutions(
    session: AsyncSession = Depends(database.get_async_session),  # noqa: B008
) -> list[dict[str, str | None]]:
    """List all institutions."""
    result = await session.execute(select(Institution))
    institutions = result.scalars().all()

    return [
        {
            "id": str(inst.id),
            "name": inst.name,
            "slug": inst.slug,
            "website": inst.website,
            "logo_url": inst.logo_url,
        }
        for inst in institutions
    ]


@router.get("/{institution_id}", response_model=dict[str, Any])
async def get_institution(
    institution_id: UUID,
    session: AsyncSession = Depends(database.get_async_session),  # noqa: B008
) -> dict[str, Any]:
    """Get a specific institution by ID."""
    institution = await session.get(Institution, institution_id)

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    return {
        "id": str(institution.id),
        "name": institution.name,
        "slug": institution.slug,
        "website": institution.website,
        "logo_url": institution.logo_url,
        "created_at": institution.created_at,
        "updated_at": institution.updated_at,
    }
