from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.services import example_service

router = APIRouter()


@router.get("")
async def get_users(
    *,
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
    user_ids: list[int] | None = Query(default=None),  # noqa: B008
):
    users = await example_service.get_users()
    return users
