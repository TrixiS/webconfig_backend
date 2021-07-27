from typing import Generator

from fastapi import APIRouter
from fastapi.params import Depends

from ..web_config import WebConfig, Config, Phrases

router = APIRouter()
schema = WebConfig.schema()


async def use_config() -> Generator:
    try:
        yield WebConfig._instance
    finally:
        await WebConfig._instance.save()


@router.get("/schema", status_code=200)
async def get_schema():
    return schema


@router.get("/config", status_code=200)
async def get_config():
    return WebConfig._instance.config


@router.get("/phrases", status_code=200)
async def get_phrases():
    return WebConfig._instance.phrases


@router.post("/config", status_code=200)
async def post_config(config: Config, web_config: WebConfig = Depends(use_config)):
    web_config.config = config


@router.post("/phrases", status_code=200)
async def post_phrases(phrases: Phrases, web_config: WebConfig = Depends(use_config)):
    web_config.phrases = phrases
