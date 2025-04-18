from modelcontextprotocol import Server
from modelcontextprotocol.adapters.redis import RedisAdapter
import asyncio
import redis.asyncio as redis


class CustomRedisAdapter(RedisAdapter):
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        super().__init__(redis_url)

    async def get(self, key: str):
        value = await self.redis_client.get(key)
        print(f"Retrieved: {key}")
        return value

    async def set(self, key: str, value: str):
        print(f"Storing: {key}")
        await self.redis_client.set(key, value)


async def main():
    redis_url = "redis://localhost:6379"
    adapter = CustomRedisAdapter(redis_url)
    server = Server(adapter)

    print(f"Starting custom MCP server with Redis at {redis_url}")
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())