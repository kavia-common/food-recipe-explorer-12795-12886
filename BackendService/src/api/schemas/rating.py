from typing import Optional
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class RatingCreate(BaseModel):
    """Create a user rating for a food item."""
    item_id: str = Field(..., description="Food item ID")
    score: int = Field(..., ge=1, le=5, description="Rating score between 1 and 5")
    comment: Optional[str] = Field(None, description="Optional rating comment")


# PUBLIC_INTERFACE
class RatingOut(BaseModel):
    """Rating response schema."""
    id: str = Field(..., description="Rating ID")
    item_id: str = Field(..., description="Food item ID")
    user_id: str = Field(..., description="User ID that submitted the rating")
    score: int = Field(..., ge=1, le=5, description="Rating score")
    comment: Optional[str] = Field(None, description="Comment")
