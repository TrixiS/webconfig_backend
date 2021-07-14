from fastapi import APIRouter

from app import web_config
from ..web_config import WebConfig

router = APIRouter()
schema = WebConfig.schema()

# TODO:
# - endpoint for taking last launch error
# - browser event for that error
# - bworter event for start
# -               and stop


@router.get("/schema", status_code=200)
async def get_schema():
    return schema


@router.get("/config", status_code=200)
async def get_config():
    return web_config
