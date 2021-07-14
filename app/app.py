from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import config
from .settings import settings

app = FastAPI()
app.include_router(config.router)

# TODO: disable logs
# TODO: move config into app directory
#       push into the repo

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
