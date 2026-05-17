import asyncio
from fastapi import FastAPI
from modules.identity.endpoints import auth_api, role_router, user_router
from modules.organizations.router import org_router
from modules.projects.router import projects_router
from modules.tasks.router import task_router
from contextlib import asynccontextmanager
from core.realtime.api import websocket
from core.realtime.dependencies import manager
from core.realtime.infrastructure.redis import redis
from core.realtime.infrastructure.redis_pubsub import RedisPubSubListener


@asynccontextmanager
async def lifespan(app: FastAPI):

    listener = RedisPubSubListener(
        redis=redis,
        manager=manager,
    )

    listener_task = asyncio.create_task(
        listener.start()
    )

    yield

    listener_task.cancel()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_api.router)
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(org_router.router)
app.include_router(projects_router.router)
app.include_router(task_router.router)
app.include_router(websocket.router)