from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Public endpoint to verify API is operational.

    Returns:
        JSON response with status
    """
    return {"status": "ok"}
