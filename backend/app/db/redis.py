import redis.asyncio as redis
from ..core.config import get_settings

settings = get_settings()


class RedisCache:
    def __init__(self):
        self.redis: redis.Redis = None

    async def connect(self):
        if not self.redis:
            self.redis = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
            )
        return self.redis

    async def get(self, key: str) -> str | None:
        client = await self.connect()
        return await client.get(key)

    async def set(self, key: str, value: str, expire: int = 3600):
        client = await self.connect()
        await client.set(key, value, ex=expire)

    async def delete(self, key: str):
        client = await self.connect()
        await client.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()


redis_cache = RedisCache()
