from fastapi import FastAPI
from modules.identity.endpoints import auth_api

app = FastAPI()

app.include_router(auth_api.router)