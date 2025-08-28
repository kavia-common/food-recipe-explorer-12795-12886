from typing import List, Optional, Tuple
from uuid import uuid4

from ..repositories.memory_repo import InMemoryRepository
from ..models.domain import FoodItem
from ..schemas.food import FoodItemCreate, FoodItemUpdate


class ItemsService:
    """Business logic for food items."""

    def __init__(self, repo: InMemoryRepository):
        self.repo = repo

    def create_item(self, payload: FoodItemCreate) -> FoodItem:
        item = FoodItem(
            id=str(uuid4()),
            name=payload.name,
            description=payload.description,
            category=payload.category,
            price=payload.price,
            currency=payload.currency,
            location=payload.location,
            tags=payload.tags or [],
        )
        return self.repo.create_item(item)

    def update_item(self, item_id: str, payload: FoodItemUpdate) -> Optional[FoodItem]:
        def mutate(i: FoodItem):
            if payload.name is not None:
                i.name = payload.name
            if payload.description is not None:
                i.description = payload.description
            if payload.category is not None:
                i.category = payload.category
            if payload.price is not None:
                i.price = payload.price
            if payload.currency is not None:
                i.currency = payload.currency
            if payload.location is not None:
                i.location = payload.location
            if payload.tags is not None:
                i.tags = payload.tags

        return self.repo.update_item(item_id, mutate)

    def delete_item(self, item_id: str) -> bool:
        return self.repo.delete_item(item_id)

    def get_item(self, item_id: str) -> Optional[FoodItem]:
        return self.repo.get_item(item_id)

    def query_items(
        self,
        q: Optional[str],
        category: Optional[str],
        location: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
        min_rating: Optional[float],
        max_rating: Optional[float],
        tags: Optional[List[str]],
        sort_by: Optional[str],
        sort_order: Optional[str],
        page: int,
        per_page: int,
    ) -> Tuple[List[FoodItem], int]:
        results = self.repo.query_items(
            q=q,
            category=category,
            location=location,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            max_rating=max_rating,
            tags=tags,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        total = len(results)
        start = (page - 1) * per_page
        end = start + per_page
        return results[start:end], total
