import asyncio
from datetime import datetime
from functools import wraps

from core.caching.client import redis
from core.config import settings
from celery_app import app

from celery.utils.log import get_logger

logger = get_logger(__name__)


def run_async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@app.task(name="clear_users_inventory")
@run_async_task
async def clear_users_inventory():
    pattern = f"{settings.cache.namespace.user_inventory}:*"
    cursor = 1
    total_deleted = 0

    while cursor:
        cursor, keys = await redis.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            total_deleted += await redis.unlink(*keys)

    logger.info(f"Users inventory cache cleared at {datetime.now().isoformat}. Deleted keys: {total_deleted}")
