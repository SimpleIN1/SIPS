
from django.conf import settings

from redis import from_url as from_url_sync_redis
from redis.asyncio import from_url as from_url_async_redis


async_redis_client = from_url_async_redis(settings.LOGS_REDIS_URL, decode_responses=True)
sync_redis_client = from_url_sync_redis(settings.LOGS_REDIS_URL, decode_responses=True)
