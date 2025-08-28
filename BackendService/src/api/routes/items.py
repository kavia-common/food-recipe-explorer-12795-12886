from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..schemas.food import (
    FoodItemCreate,
    FoodItemUpdate,
    FoodItemOut,
    FoodItemQuery,
    PaginatedResponse,
)
from ..repositories.memory_repo import InMemoryRepository
from ..services.items_service import ItemsService
from ..core.dependencies import get_pagination, get_sorting, get_required_user, get_optional_user
from ..core.security import AuthUser, ensure_admin

router = APIRouter()

# Dependency
def get_service(repo: InMemoryRepository = Depends(lambda: InMemoryRepository())) -> ItemsService:
    return ItemsService(repo)

# PUBLIC_INTERFACE
@router.post("", response_model=FoodItemOut, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    payload: FoodItemCreate,
    service: ItemsService = Depends(get_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Create a new food item.
    Requires admin privileges.
    """
    ensure_admin(user)
    item = service.create_item(payload)
    return item

# PUBLIC_INTERFACE
@router.get("", response_model=List[FoodItemOut])
async def list_food_items(
    query: FoodItemQuery = Depends(),
    pagination: dict = Depends(get_pagination),
    sorting: dict = Depends(get_sorting),
    service: ItemsService = Depends(get_service),
    _: AuthUser | None = Depends(get_optional_user),
) -> List[FoodItemOut]:
    """
    List and search food items with filtering, sorting, and pagination.
    No authentication required.
    """
    items, total = service.query_items(
        q=query.q,
        category=query.category,
        location=query.location,
        min_price=query.min_price,
        max_price=query.max_price,
        min_rating=query.min_rating,
        max_rating=query.max_rating,
        tags=query.tags,
        sort_by=sorting.sort_by,
        sort_order=sorting.sort_order,
        page=pagination.page,
        per_page=pagination.per_page,
    )
    return PaginatedResponse(
        items=items,
        page=pagination.page,
        per_page=pagination.per_page,
        total=total,
    ).model_dump()

# PUBLIC_INTERFACE
@router.get("/{item_id}", response_model=FoodItemOut)
async def get_food_item(
    item_id: str,
    service: ItemsService = Depends(get_service),
    _: AuthUser | None = Depends(get_optional_user),
):
    """
    Get details for a specific food item.
    No authentication required.
    """
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )
    return item

# PUBLIC_INTERFACE
@router.patch("/{item_id}", response_model=FoodItemOut)
async def update_food_item(
    item_id: str,
    payload: FoodItemUpdate,
    service: ItemsService = Depends(get_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Update a food item.
    Requires admin privileges.
    """
    ensure_admin(user)
    item = service.update_item(item_id, payload)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )
    return item

# PUBLIC_INTERFACE
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(
    item_id: str,
    service: ItemsService = Depends(get_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Delete a food item.
    Requires admin privileges.
    """
    ensure_admin(user)
    if not service.delete_item(item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found",
        )
