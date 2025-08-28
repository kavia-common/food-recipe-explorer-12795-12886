from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class FoodItem:
    id: str
    name: str
    description: str
    category: str
    price: float
    currency: str
    location: str
    tags: List[str] = field(default_factory=list)
    avg_rating: float = 0.0
    rating_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Rating:
    id: str
    item_id: str
    user_id: str
    score: int
    comment: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Feedback:
    id: str
    item_id: str
    user_id: str
    message: str
    status: str = "pending"  # pending | approved | rejected
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
