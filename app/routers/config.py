from typing import Generator

from fastapi import APIRouter
from fastapi.params import Depends

from ..web_config import WebConfig, Config, Phrases

router = APIRouter()
schema = WebConfig.schema()

# TODO:
# - endpoint for taking last launch error
# - browser event for that error
# - bworter event for start
# -               and stop


async def use_config() -> Generator:
    try:
        yield WebConfig.instance
    finally:
        await WebConfig.instance.save()


@router.get("/schema", status_code=200)
async def get_schema():
    return schema


@router.get("/config", status_code=200)
async def get_config():
    return WebConfig.instance.config


@router.get("/phrases", status_code=200)
async def get_phrases():
    return WebConfig.instance.phrases


@router.post("/config", status_code=200)
async def post_config(config: Config, web_config: WebConfig = Depends(use_config)):
    web_config.config = config


@router.post("/phrases", status_code=200)
async def post_phrases(phrases: Phrases, web_config: WebConfig = Depends(use_config)):
    web_config.phrases = phrases
