import aioredis
import databases

from pyzer import settings

database = databases.Database(settings.DB_DSN)

redis_sessions_db = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
