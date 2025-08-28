from typing import Optional
from fastapi import Query, Depends
from pydantic import BaseModel, Field

from .security import mock_get_current_user_optional, mock_get_current_user_required, AuthUser


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""
    page: int = Field(1, ge=1, description="Page number (1-based)")
    per_page: int = Field(10, ge=1, le=100, description="Items per page (max 100)")


class SortParams(BaseModel):
    """Sorting parameters."""
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field(None, description="Sort order: asc|desc")


def get_pagination(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
) -> PaginationParams:
    """Get pagination parameters."""
    return PaginationParams(page=page, per_page=per_page)


def get_sorting(
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_order: Optional[str] = Query(None, pattern="^(asc|desc)$", description="Sort order (asc|desc)"),
) -> SortParams:
    """Get sorting parameters."""
    return SortParams(sort_by=sort_by, sort_order=sort_order)


async def get_optional_user(
    user: Optional[AuthUser] = Depends(mock_get_current_user_optional)
) -> Optional[AuthUser]:
    """Optional user dependency (no error if not authenticated)."""
    return user


async def get_required_user(
    user: AuthUser = Depends(mock_get_current_user_required)
) -> AuthUser:
    """Required user dependency (raise 401 if not authenticated)."""
    return user
