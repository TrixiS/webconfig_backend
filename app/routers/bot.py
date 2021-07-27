import asyncio
import threading

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from ..web_config import WebConfig
from ..singleton import Singleton
from ..sse import SSEvent
from ..discord_bot import Bot, BotState, BotStatus

router = APIRouter()


class BotThread(threading.Thread, Singleton):
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
        SSEvent.instance().send(
            BotStatus(id=id(BotThread.instance()), status=BotState.loading)
        )

        asyncio.set_event_loop(self.loop)

        if self.bot is None:
            self.bot = Bot(WebConfig._instance, loop=self.loop)

        self.bot.run()

    def stop(self):
        self.loop.create_task(self.bot.close())


async def status_event_generator(request: Request):
    while True:
        await SSEvent.instance().wait()

        if await request.is_disconnected():
            break

        yield {
            "event": "update",
            "retry": 30000,
            "data": SSEvent.instance().data.json(),
        }


@router.get("", status_code=200, response_model=BotStatus)
async def bot_get():
    return BotStatus(id=id(BotThread.instance()), status=BotThread.instance().bot_state)


@router.get("/status")
async def bot_status_stream(request: Request):
    event_generator = status_event_generator(request)
    return EventSourceResponse(event_generator)


@router.post("/start", status_code=200)
async def bot_start():
    if BotThread.instance().bot_state.running:
        return

    BotThread.instance(new=True).start()


@router.post("/restart", status_code=200)
async def bot_reload():
    if BotThread.has_instance():
        BotThread.instance().stop()

    BotThread.instance(new=True).start()


@router.post("/stop", status_code=200)
async def bot_stop():
    if (
        not BotThread.has_instance()
        or BotThread.instance().bot_state is BotState.stopped
    ):
        return

    BotThread.instance().stop()
