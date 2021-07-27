import threading

from enum import Enum

from pydantic import BaseModel

from bot.bot import Bot as _Bot
from .sse import SSEvent


class BotState(str, Enum):
    ready = "ready"
    loading = "loading"
    stopped = "stopped"
    unknown = "unknown"

    @property
    def running(self) -> bool:
        return self is BotState.ready or self is BotState.loading


class BotStatus(BaseModel):
    id: int
    status: BotState


class Bot(_Bot):
    async def on_ready(self):
        await super().on_ready()
        thread = threading.current_thread()
        SSEvent.instance().send(BotStatus(id=id(thread), status=BotState.ready))

    async def close(self):
        thread = threading.current_thread()
        SSEvent.instance().send(BotStatus(id=id(thread), status=BotState.stopped))
        await super().close()
