from typing import List, Optional
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class FoodItemBase(BaseModel):
    """Common fields for food items."""
    name: str = Field(..., description="Food item name")
    description: str = Field(..., description="Food item description")
    category: str = Field(..., description="Category (e.g., Dessert, Main Course)")
    price: float = Field(..., ge=0, description="Price value")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (e.g., USD)")
    location: str = Field(..., description="Location associated with the item")
    tags: List[str] = Field(default_factory=list, description="List of tags for filtering and search")


# PUBLIC_INTERFACE
class FoodItemCreate(FoodItemBase):
    """Schema for creating a new food item."""
    pass


# PUBLIC_INTERFACE
class FoodItemUpdate(BaseModel):
    """Schema for updating a food item."""
    name: Optional[str] = Field(None, description="Food item name")
    description: Optional[str] = Field(None, description="Food item description")
    category: Optional[str] = Field(None, description="Category")
    price: Optional[float] = Field(None, ge=0, description="Price value")
    currency: Optional[str] = Field(None, min_length=3, max_length=3, description="Currency code")
    location: Optional[str] = Field(None, description="Location")
    tags: Optional[List[str]] = Field(None, description="Tags")


# PUBLIC_INTERFACE
class FoodItemOut(FoodItemBase):
    """Schema for returning food item data."""
    id: str = Field(..., description="Food item ID")
    avg_rating: float = Field(..., ge=0, le=5, description="Average rating")
    rating_count: int = Field(..., ge=0, description="Total rating count")


# PUBLIC_INTERFACE
class FoodItemQuery(BaseModel):
    """Query params for searching/filtering/sorting food items."""
    q: Optional[str] = Field(None, description="Search text across name, description, tags")
    category: Optional[str] = Field(None, description="Filter by category")
    location: Optional[str] = Field(None, description="Filter by location")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum average rating")
    max_rating: Optional[float] = Field(None, ge=0, le=5, description="Maximum average rating")
    tags: Optional[List[str]] = Field(None, description="Tags to include")
    sort_by: Optional[str] = Field(None, description="Sort field (name, price, avg_rating, created_at)")
    sort_order: Optional[str] = Field(None, description="Sort order (asc|desc)")


# PUBLIC_INTERFACE
class PaginatedResponse(BaseModel):
    """Generic pagination response container."""
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, description="Items per page")
    total: int = Field(..., ge=0, description="Total items")
