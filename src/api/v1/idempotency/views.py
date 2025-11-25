from fastapi import APIRouter

from api.v1.idempotency.schemas import IdempotencyKeyModel

router = APIRouter(prefix="/idempotency", tags=["idempotency gen"])


@router.get("/generate-key/", response_model=IdempotencyKeyModel)
async def generate_key() -> IdempotencyKeyModel:
    """Так как фронта нет, но нужно как-то генерировать idempotency_key"""
    return IdempotencyKeyModel()
