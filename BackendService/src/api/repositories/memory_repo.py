from __future__ import annotations
from typing import Dict, List, Optional, Iterable, Callable
from uuid import uuid4
from datetime import datetime

from ..models.domain import FoodItem, Rating, Feedback


class InMemoryRepository:
    """
    Simple in-memory repository to simulate persistence.
    Thread-safety is not addressed for simplicity in this mock.
    """

    def __init__(self):
        self.items: Dict[str, FoodItem] = {}
        self.ratings: Dict[str, Rating] = {}
        self.feedbacks: Dict[str, Feedback] = {}

        # Seed with example items
        self._seed_items()

    def _seed_items(self):
        seed = [
            FoodItem(
                id=str(uuid4()),
                name="Margherita Pizza",
                description="Classic pizza with tomatoes, mozzarella, and basil.",
                category="Main Course",
                price=12.5,
                currency="USD",
                location="Naples",
                tags=["pizza", "italian", "vegetarian"],
                avg_rating=4.5,
                rating_count=10,
            ),
            FoodItem(
                id=str(uuid4()),
                name="Sushi Platter",
                description="Assorted sushi with fresh fish and rice.",
                category="Main Course",
                price=22.0,
                currency="USD",
                location="Tokyo",
                tags=["sushi", "japanese", "seafood"],
                avg_rating=4.7,
                rating_count=25,
            ),
            FoodItem(
                id=str(uuid4()),
                name="Chocolate Lava Cake",
                description="Warm chocolate cake with molten center.",
                category="Dessert",
                price=7.0,
                currency="USD",
                location="Paris",
                tags=["dessert", "chocolate"],
                avg_rating=4.2,
                rating_count=18,
            ),
        ]
        for s in seed:
            self.items[s.id] = s

    # FoodItem operations
    def create_item(self, item: FoodItem) -> FoodItem:
        self.items[item.id] = item
        return item

    def update_item(self, item_id: str, mutator: Callable[[FoodItem], None]) -> Optional[FoodItem]:
        item = self.items.get(item_id)
        if not item:
            return None
        mutator(item)
        item.updated_at = datetime.utcnow()
        return item

    def delete_item(self, item_id: str) -> bool:
        return self.items.pop(item_id, None) is not None

    def get_item(self, item_id: str) -> Optional[FoodItem]:
        return self.items.get(item_id)

    def list_items(self) -> Iterable[FoodItem]:
        return list(self.items.values())

    # Rating operations
    def add_rating(self, rating: Rating) -> Rating:
        self.ratings[rating.id] = rating
        # Update aggregate on item
        item = self.items.get(rating.item_id)
        if item:
            total_score = item.avg_rating * item.rating_count + rating.score
            item.rating_count += 1
            item.avg_rating = round(total_score / item.rating_count, 2)
            item.updated_at = datetime.utcnow()
        return rating

    def list_ratings_for_item(self, item_id: str) -> List[Rating]:
        return [r for r in self.ratings.values() if r.item_id == item_id]

    # Feedback operations
    def add_feedback(self, feedback: Feedback) -> Feedback:
        self.feedbacks[feedback.id] = feedback
        return feedback

    def list_feedback_for_item(self, item_id: str) -> List[Feedback]:
        return [f for f in self.feedbacks.values() if f.item_id == item_id]

    def set_feedback_status(self, feedback_id: str, status: str) -> Optional[Feedback]:
        fb = self.feedbacks.get(feedback_id)
        if not fb:
            return None
        fb.status = status
        fb.updated_at = datetime.utcnow()
        return fb

    # Query utilities
    def query_items(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        location: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        tags: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[FoodItem]:
        items = list(self.items.values())

        def matches(item: FoodItem) -> bool:
            if q:
                ql = q.lower()
                if not (
                    ql in item.name.lower()
                    or ql in item.description.lower()
                    or any(ql in t.lower() for t in item.tags)
                ):
                    return False
            if category and item.category.lower() != category.lower():
                return False
            if location and item.location.lower() != location.lower():
                return False
            if min_price is not None and item.price < min_price:
                return False
            if max_price is not None and item.price > max_price:
                return False
            if min_rating is not None and item.avg_rating < min_rating:
                return False
            if max_rating is not None and item.avg_rating > max_rating:
                return False
            if tags and not set(tag.lower() for tag in tags).issubset(set(t.lower() for t in item.tags)):
                return False
            return True

        filtered = [i for i in items if matches(i)]

        if sort_by:
            reverse = (sort_order or "asc").lower() == "desc"
            key_map = {
                "name": lambda x: x.name.lower(),
                "price": lambda x: x.price,
                "avg_rating": lambda x: x.avg_rating,
                "created_at": lambda x: x.created_at,
            }
            key_fn = key_map.get(sort_by)
            if key_fn:
                filtered.sort(key=key_fn, reverse=reverse)

        return filtered
