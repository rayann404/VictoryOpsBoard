from fastapi import FastAPI
from modules.identity.endpoints import auth_api, role_router, user_router
from modules.organizations.router import org_router
from modules.projects.router import projects_router
from modules.tasks.router import task_router
from modules.ai.endpoints import ai_api
from google import genai
from contextlib import asynccontextmanager
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.gemini = genai.Client(api_key=settings.GEMINI_API_KEY)
    yield
    await app.state.gemini.aio.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_api.router)
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(org_router.router)
app.include_router(projects_router.router)
app.include_router(task_router.router)
app.include_router(ai_api)
