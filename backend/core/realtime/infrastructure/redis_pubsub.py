import orjson

from redis.asyncio import Redis

from realtime.infrastructure.manager import (
    ConnectionManager,
)


class RedisPubSubListener:

    def __init__(
        self,
        redis: Redis,
        manager: ConnectionManager,
    ):
        self.redis = redis
        self.manager = manager

    async def start(self):

        pubsub = self.redis.pubsub()

        await pubsub.psubscribe(
            "project:*",
        )

        async for message in pubsub.listen():
            if message["type"] != "pmessage":
                continue

            channel = (
                message["channel"]
                .decode()
            )

            data = orjson.loads(
                message["data"]
            )

            await self.manager.broadcast(
                channel=channel,
                message=data,
            )