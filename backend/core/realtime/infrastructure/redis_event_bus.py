import orjson

from redis.asyncio import Redis

from realtime.services.event_bus import EventBus


class RedisEventBus(EventBus):

    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def publish(
        self,
        channel: str,
        event: dict,
    ) -> None:

        await self.redis.publish(
            channel,
            orjson.dumps(event),
        )