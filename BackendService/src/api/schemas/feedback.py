
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class FeedbackCreate(BaseModel):
    """Create a feedback entry for a food item."""
    item_id: str = Field(..., description="Food item ID")
    message: str = Field(..., min_length=1, description="Feedback message")


# PUBLIC_INTERFACE
class FeedbackOut(BaseModel):
    """Feedback response schema."""
    id: str = Field(..., description="Feedback ID")
    item_id: str = Field(..., description="Food item ID")
    user_id: str = Field(..., description="User ID that submitted the feedback")
    message: str = Field(..., description="Feedback message")
    status: str = Field(..., description="Moderation status (pending|approved|rejected)")
