import pickle
import uuid
from typing import Annotated

from fastapi import Path, Header

from api.v1.users.schemas import AddFundsBodyModel, AddFundsModel
from core.caching.client import redis
from core.config import settings


async def get_user_inventory_from_cache(
        user_id: Annotated[int, Path(ge=1, title="User id")]
) -> list[dict] | None:
    key = f"{settings.cache.namespace.user_inventory}:{user_id}"
    from_cache = await redis.get(key)
    if from_cache:
        return pickle.loads(from_cache)
    return None


def add_funds_payload(
    user_id: Annotated[int, Path(ge=1, title="User ID")],
    idempotency_key: Annotated[uuid.UUID, Header(alias="Idempotency-Key")],
    body: AddFundsBodyModel,
):
    return AddFundsModel(
        user_id=user_id,
        idempotency_key=idempotency_key,
        **body.model_dump(),
    )
