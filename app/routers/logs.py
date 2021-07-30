import threading
import traceback
import logging

from io import StringIO

from fastapi import APIRouter
from pydantic import BaseModel

exc_buffer = StringIO()
buffer_handler = logging.StreamHandler(exc_buffer)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    handlers=[buffer_handler],
)

threading.excepthook = lambda args: logging.error(
    "".join(
        traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
    )
)

router = APIRouter()


class Logs(BaseModel):
    text: str


# TODO: send stream of the log file (dont use buffers)
@router.get("", status_code=200, response_model=Logs)
async def logs_get():
    exc_buffer.seek(0)
    return Logs(text=exc_buffer.read())
