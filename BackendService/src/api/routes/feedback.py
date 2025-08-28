from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas.feedback import FeedbackCreate, FeedbackOut
from ..repositories.memory_repo import InMemoryRepository
from ..services.feedback_service import FeedbackService
from ..core.dependencies import get_required_user
from ..core.security import AuthUser

router = APIRouter()

# Dependency
def get_service(repo: InMemoryRepository = Depends(lambda: InMemoryRepository())) -> FeedbackService:
    return FeedbackService(repo)

# PUBLIC_INTERFACE
@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    payload: FeedbackCreate,
    service: FeedbackService = Depends(get_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Create a new feedback for a food item.
    Requires authentication.
    """
    feedback = service.add_feedback(user.id, payload)
    return feedback

# PUBLIC_INTERFACE
@router.get("/item/{item_id}", response_model=List[FeedbackOut])
async def list_item_feedback(
    item_id: str,
    service: FeedbackService = Depends(get_service),
    _: AuthUser = Depends(get_required_user),
):
    """
    List all feedback for a specific food item.
    Requires authentication.
    """
    return service.list_for_item(item_id)
