import threading
import traceback
import logging

import aiofiles

from fastapi import APIRouter
from pydantic import BaseModel

from bot import root_path

log_path = root_path / "logs.log"

logging.basicConfig(
    filename=str(log_path),
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

threading.excepthook = lambda args: logging.error(
    "".join(
        traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
    )
)

router = APIRouter()


class Logs(BaseModel):
    text: str


@router.get("", response_model=Logs)
async def logs_get():
    async with aiofiles.open(log_path, "r", encoding="utf-8") as f:
        logs_text = await f.read()
        return Logs(text=logs_text.strip())


@router.delete("")
async def logs_delete():
    async with aiofiles.open(log_path, "w", encoding="utf-8") as f:
        await f.write("")
