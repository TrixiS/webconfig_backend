from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from .routers import config, bot
from .web_config import WebConfig

app = FastAPI()
app.include_router(config.router)
app.include_router(bot.router, prefix="/bot")

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
    WebConfig._instance = await WebConfig.load()


@app.on_event("shutdown")
async def on_shutdown():
    await WebConfig._instance.save()
