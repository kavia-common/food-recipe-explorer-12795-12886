from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas.rating import RatingCreate, RatingOut
from ..repositories.memory_repo import InMemoryRepository
from ..services.ratings_service import RatingsService
from ..core.dependencies import get_required_user
from ..core.security import AuthUser

router = APIRouter()

# Dependency
def get_service(repo: InMemoryRepository = Depends(lambda: InMemoryRepository())) -> RatingsService:
    return RatingsService(repo)

# PUBLIC_INTERFACE
@router.post("", response_model=RatingOut, status_code=status.HTTP_201_CREATED)
async def create_rating(
    payload: RatingCreate,
    service: RatingsService = Depends(get_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Create a new rating for a food item.
    Requires authentication.
    """
    rating = service.add_rating(user.id, payload)
    return rating

# PUBLIC_INTERFACE
@router.get("/item/{item_id}", response_model=List[RatingOut])
async def list_item_ratings(
    item_id: str,
    service: RatingsService = Depends(get_service),
    _: AuthUser = Depends(get_required_user),
):
    """
    List all ratings for a specific food item.
    Requires authentication.
    """
    return service.list_for_item(item_id)
