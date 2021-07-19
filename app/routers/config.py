from typing import Generator

from fastapi import APIRouter
from fastapi.params import Depends

from app import app
from ..web_config import WebConfig, Config, Phrases, save_config

router = APIRouter()
schema = WebConfig.schema()

# TODO:
# - endpoint for taking last launch error
# - browser event for that error
# - bworter event for start
# -               and stop


async def use_config() -> Generator:
    try:
        yield app.web_config
    finally:
        await save_config(app.web_config)


@router.get("/schema", status_code=200)
async def get_schema():
    return schema


@router.get("/config", status_code=200)
async def get_config():
    return app.web_config.config


@router.get("/phrases", status_code=200)
async def get_phrases():
    return app.web_config.phrases


@router.post("/config", status_code=200)
async def post_config(config: Config, web_config: WebConfig = Depends(use_config)):
    web_config.config = config


@router.post("/phrases", status_code=200)
async def post_phrases(phrases: Phrases, web_config: WebConfig = Depends(use_config)):
    web_config.phrases = phrases
