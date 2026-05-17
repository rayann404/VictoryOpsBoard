from typing import Protocol


class EventBus(Protocol):

    async def publish(
        self,
        channel: str,
        event: dict,
    ) -> None:
        ...