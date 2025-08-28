from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ..core.dependencies import get_required_user
from ..core.security import AuthUser

router = APIRouter()

class TokenResponse(BaseModel):
    """Mock token response."""
    access_token: str = Field(..., description="Mock access token")
    token_type: str = Field("bearer", description="Token type")

# PUBLIC_INTERFACE
@router.post("/token", response_model=TokenResponse)
async def mock_login(email: str):
    """
    Mock login endpoint that returns a simple test token.
    Format: user:<uuid>:<email> for regular users
           admin:<uuid>:<email> for admin users
    """
    # Simulate admin for test@admin.com
    is_admin = email.lower() == "test@admin.com"
    role = "admin" if is_admin else "user"
    uid = "12345" if is_admin else "67890"  # Mock IDs
    token = f"{role}:{uid}:{email}"
    return TokenResponse(access_token=token)

# PUBLIC_INTERFACE
@router.get("/me", response_model=AuthUser)
async def get_current_user(user: AuthUser = Depends(get_required_user)):
    """Get current authenticated user info."""
    return user
