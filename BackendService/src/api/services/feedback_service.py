from typing import List, Optional
from uuid import uuid4

from ..repositories.memory_repo import InMemoryRepository
from ..models.domain import Feedback
from ..schemas.feedback import FeedbackCreate


class FeedbackService:
    """Business logic for feedback."""

    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def add_feedback(self, user_id: str, payload: FeedbackCreate) -> Feedback:
        feedback = Feedback(
            id=str(uuid4()),
            item_id=payload.item_id,
            user_id=user_id,
            message=payload.message,
        )
        return self.repo.add_feedback(feedback)

    def list_for_item(self, item_id: str) -> List[Feedback]:
        return self.repo.list_feedback_for_item(item_id)

    def set_status(self, feedback_id: str, status: str) -> Optional[Feedback]:
        return self.repo.set_feedback_status(feedback_id, status)
