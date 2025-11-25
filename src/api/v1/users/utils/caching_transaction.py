import json

from api.v1.users.schemas import AddFundsResponseModel
from core.caching.client import redis
from core.config import settings


class CachingTransaction:
    IDEMPOTENCY_KEY_TTL = 60 * 30

    def __init__(self, idempotency_key: str, user_id: int, **kwargs):  # NOQA
        self.key = f"{settings.cache.namespace.idempotency_key}:{user_id}:{idempotency_key}"

    async def get_value(self) -> AddFundsResponseModel | None:
        cached_result_json = await redis.get(self.key)
        if cached_result_json:
            cached_result = json.loads(cached_result_json)
            return AddFundsResponseModel(**cached_result)
        return None

    async def set_value(self, value: AddFundsResponseModel):
        await redis.set(self.key, value.model_dump_json(), ex=self.IDEMPOTENCY_KEY_TTL)
