from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import config
from .settings import settings
from .web_config import load_config, save_config

app = FastAPI()
app.include_router(config.router)

web_config = None

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def on_startup():
    global web_config
    web_config = await load_config()


@app.on_event("shutdown")
async def on_shutdown():
    global web_config
    await save_config(web_config)
