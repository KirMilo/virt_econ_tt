from celery import Celery
from celery.schedules import crontab
from core.config import settings
from celery.utils.log import get_logger

logger = get_logger(__name__)

app = Celery(
    'celery_worker',
    broker="redis://{host}:{port}/1".format(**settings.redis.model_dump(exclude={"db"})),
)
app.autodiscover_tasks(["src.beat_tasks"])

app.conf.beat_schedule = {
    'clear_users_inventory_cache_per_day': {
        'task': 'clear_users_inventory',
        'schedule': crontab(hour=0, minute=0),
        'args': (),
    },
}

app.conf.timezone = 'Europe/Moscow'
