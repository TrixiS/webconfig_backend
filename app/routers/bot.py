from fastapi import APIRouter, Request, HTTPException
from sse_starlette.sse import EventSourceResponse

from ..discord_bot import BotState, BotStatus, BotThread, SSEvent

router = APIRouter()


class BotThreadManager:
    def __init__(self):
        self.sse = SSEvent()
        self.thread: BotThread = None

    def start(self):
        if self.thread is not None and self.thread.bot_state.running:
            raise HTTPException(400)

        self.thread = BotThread(self.sse)
        self.thread.start()

    def stop(self):
        if self.thread is None:
            raise HTTPException(400)

        self.thread.stop()
        self.thread = None


manager = BotThreadManager()


async def status_event_generator(request: Request):
    while True:
        await manager.sse.wait()

        if await request.is_disconnected():
            break

        yield {
            "event": "update",
            "retry": 30000,
            "data": manager.sse.data.json(),
        }


@router.get("", status_code=200, response_model=BotStatus)
async def bot_get():
    if manager.thread is None:
        return BotStatus(id=None, status=BotState.stopped)

    return BotStatus(id=id(manager.thread), status=manager.thread.bot_state)


@router.get("/status")
async def bot_status_stream(request: Request):
    event_generator = status_event_generator(request)
    return EventSourceResponse(event_generator)


@router.post("/start", status_code=200)
async def bot_start():
    manager.start()


@router.post("/restart", status_code=200)
async def bot_reload():
    manager.stop()
    manager.start()


@router.post("/stop", status_code=200)
async def bot_stop():
    manager.stop()
