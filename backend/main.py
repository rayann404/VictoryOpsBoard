from fastapi import FastAPI
from modules.identity.endpoints import auth_api, role_router, user_router
from modules.organizations.router import org_router
from modules.projects.router import projects_router
from modules.tasks.router import task_router

app = FastAPI()

app.include_router(auth_api.router)
app.include_router(role_router.router)
app.include_router(user_router.router)
app.include_router(org_router.router)
app.include_router(projects_router.router)
app.include_router(task_router.router)