from typing import List
from uuid import uuid4

from ..repositories.memory_repo import InMemoryRepository
from ..models.domain import Rating
from ..schemas.rating import RatingCreate


class RatingsService:
    """Business logic for ratings."""

    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def add_rating(self, user_id: str, payload: RatingCreate) -> Rating:
        rating = Rating(
            id=str(uuid4()),
            item_id=payload.item_id,
            user_id=user_id,
            score=payload.score,
            comment=payload.comment,
        )
        return self.repo.add_rating(rating)

    def list_for_item(self, item_id: str) -> List[Rating]:
        return self.repo.list_ratings_for_item(item_id)
