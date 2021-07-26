import asyncio
import threading

from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel

from ..web_config import WebConfig
from bot.bot import Bot

router = APIRouter()


class BotState(str, Enum):
    ready = "ready"
    loading = "loading"
    stopped = "stopped"
    unknown = "unknown"


class BotThread(threading.Thread):
    __instance__: "BotThread" = None

    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.loop = asyncio.new_event_loop()
        self.bot: Bot = None

    @property
    def bot_state(self) -> BotState:
        if self.bot is None:
            return BotState.stopped

        if self.bot.is_closed() or not self.loop.is_running() or self.loop.is_closed():
            return BotState.stopped

        if self.bot.is_ready():
            return BotState.ready

        return BotState.loading

    def run(self):
        asyncio.set_event_loop(self.loop)

        if self.bot is None:
            self.bot = Bot(WebConfig.__instance__, loop=self.loop)

        self.bot.run()

    def stop(self):
        self.loop.create_task(self.bot.close())


class BotStatus(BaseModel):
    status: BotState


@router.get("", status_code=200, response_model=BotStatus)
async def bot_get():
    if BotThread.__instance__ is None:
        return BotStatus(status=BotState.stopped)

    return BotStatus(status=BotThread.__instance__.bot_state)


@router.post("/start", status_code=200)
async def bot_start():
    if BotThread.__instance__ is not None:
        return

    BotThread.__instance__ = BotThread()
    BotThread.__instance__.start()

    # TODO: send client event on start
    # TODO: use async queue for events


@router.post("/restart", status_code=200)
async def bot_reload():
    if BotThread.__instance__ is not None:
        BotThread.__instance__.stop()

    BotThread.__instance__ = BotThread()
    BotThread.__instance__.start()


@router.post("/stop", status_code=200)
async def bot_stop():
    if BotThread.__instance__ is None:
        return

    BotThread.__instance__.stop()
    BotThread.__instance__ = None
