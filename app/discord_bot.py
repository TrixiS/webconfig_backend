import asyncio
import threading

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from bot.bot import Bot as _Bot
from .web_config import WebConfig


class SSEvent(asyncio.Event):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data: BaseModel = None

    def send(self, data):
        self.data = data
        self.set()


class BotState(str, Enum):
    ready = "ready"
    loading = "loading"
    stopped = "stopped"
    unknown = "unknown"

    @property
    def running(self) -> bool:
        return self is BotState.ready or self is BotState.loading


class BotStatus(BaseModel):
    id: Optional[int]
    status: BotState


class BotThread(threading.Thread):
    def __init__(self, sse):
        super().__init__(name=self.__class__.__name__)
        self.sse: SSEvent = sse
        self.loop: asyncio.AbstractEventLoop = None
        self.bot: Bot = None

    @property
    def bot_state(self) -> BotState:
        if (
            self.bot is None
            or self.bot.is_closed()
            or not self.loop.is_running()
            or self.loop.is_closed()
            or not self.is_alive()
        ):
            return BotState.stopped

        if self.bot.is_ready():
            return BotState.ready

        return BotState.loading

    def run(self):
        self.sse.send(BotStatus(id=id(self), status=BotState.loading))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.bot = Bot(WebConfig._instance, loop=self.loop)
        self.bot.run()

    def stop(self):
        if self.loop is None:
            return

        self.sse.send(BotStatus(id=id(self), status=BotState.loading))
        self.loop.create_task(self.bot.close())
        self.loop = None
        self.bot = None


class Bot(_Bot):
    async def on_ready(self):
        await super().on_ready()
        thread: BotThread = threading.current_thread()
        thread.sse.send(BotStatus(id=id(thread), status=BotState.ready))

    async def close(self):
        thread: BotThread = threading.current_thread()
        thread.sse.send(BotStatus(id=id(thread), status=BotState.stopped))
        await super().close()
