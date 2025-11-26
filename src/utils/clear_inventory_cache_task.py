from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from core.caching.client import redis
from core.config import settings


async def clear_users_inventory():  # TODO: Нужно протестить
    pattern = f"{settings.cache.namespace.users_inventory}:*"
    cursor = b'0'
    total_deleted = 0

    while cursor:
        cursor, keys = await redis.scan(cursor=cursor, match=pattern, count=100)
        total_deleted += await redis.unlink(*keys)

    print(f"Users inventory cache cleared. Deleted keys: {total_deleted}")


scheduler = AsyncIOScheduler()
scheduler.add_job(
    clear_users_inventory,
    CronTrigger(hour=0, minute=0),
    name="daily_clear_users_inventory",
)
