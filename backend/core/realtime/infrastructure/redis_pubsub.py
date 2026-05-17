import orjson

from redis.asyncio import Redis

from core.realtime.infrastructure.manager import (
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
        print("1️⃣ LISTENER STARTED")
        pubsub = self.redis.pubsub()

        await pubsub.psubscribe(
            "project:*",
        )
        print("2️⃣ SUBSCRIBED TO project:*")
        async for message in pubsub.listen():
            try:
                print("3️⃣ RAW MESSAGE:", message)

                if message["type"] != "pmessage":
                    continue

                channel = message["channel"].decode()
                data = orjson.loads(message["data"])

                print("4️⃣ BEFORE BROADCAST:", channel, data)

                await self.manager.broadcast(channel, data)

                print("5️⃣ AFTER BROADCAST")

            except Exception as e:
                print("❌ LISTENER ERROR:", e)