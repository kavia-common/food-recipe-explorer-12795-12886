from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import items, ratings, feedback, admin, auth
from .core.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app with metadata and OpenAPI tags
app = FastAPI(
    title="Food Recipe Explorer - BackendService",
    description=(
        "Central API for browsing, searching, filtering, sorting food items, "
        "handling ratings and feedback, with admin endpoints and auth integration points."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health check endpoints"},
        {"name": "auth", "description": "Authentication (placeholder/mock) endpoints"},
        {"name": "items", "description": "Food items browse/search/filter/sort and details"},
        {"name": "ratings", "description": "User ratings for food items"},
        {"name": "feedback", "description": "User feedback for food items"},
        {"name": "admin", "description": "Admin/moderation and data management"},
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get("/", tags=["health"], summary="Health Check", operation_id="health_check")
def health_check():
    """Simple health check endpoint returning service status."""
    return {"status": "healthy", "service": "backend", "version": settings.APP_VERSION}


# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
