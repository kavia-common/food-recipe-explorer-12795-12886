from fastapi import APIRouter, Depends, HTTPException
from enum import Enum

from ..schemas.feedback import FeedbackOut
from ..repositories.memory_repo import InMemoryRepository
from ..services.feedback_service import FeedbackService
from ..core.dependencies import get_required_user
from ..core.security import AuthUser, ensure_admin

router = APIRouter()

# Dependency
def get_feedback_service(repo: InMemoryRepository = Depends(lambda: InMemoryRepository())) -> FeedbackService:
    return FeedbackService(repo)

class FeedbackStatus(str, Enum):
    approved = "approved"
    rejected = "rejected"

# PUBLIC_INTERFACE
@router.patch("/feedback/{feedback_id}/status", response_model=FeedbackOut)
async def moderate_feedback(
    feedback_id: str,
    status: FeedbackStatus,
    service: FeedbackService = Depends(get_feedback_service),
    user: AuthUser = Depends(get_required_user),
):
    """
    Moderate a feedback item (approve/reject).
    Requires admin privileges.
    """
    ensure_admin(user)
    feedback = service.set_status(feedback_id, status.value)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )
    return feedback
