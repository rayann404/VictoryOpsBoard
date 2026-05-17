from realtime.infrastructure.manager import ConnectionManager

from realtime.infrastructure.redis import redis

from realtime.infrastructure.redis_event_bus import RedisEventBus

from realtime.services.realtime_service import RealtimeService

manager = ConnectionManager()


def get_event_bus():
    event_bus = RedisEventBus(redis)
    return event_bus


def get_realtime_service():
    realtime_service = RealtimeService(
        manager=manager,
    )
    return realtime_service
