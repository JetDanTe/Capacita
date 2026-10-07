from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["status"])



@router.api_route("", methods=["GET", "HEAD"])
async def health() -> dict[str, str]:
    return {"status": "ok"}