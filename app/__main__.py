import threading
import traceback
import logging

from uvicorn import Config, Server

from . import loop
from .app import app
from .settings import settings
from bot import root_path

logging.basicConfig(
    filename=root_path / "logs.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)


def threading_exceptions_handler(args: threading.ExceptHookArgs):
    ext_format = traceback.format_exception(
        args.exc_type, args.exc_value, args.exc_traceback
    )

    logging.error("".join(ext_format))


threading.excepthook = threading_exceptions_handler
config = Config(app, port=settings.APP_PORT, loop=loop, log_level="critical")
server = Server(config)

loop.run_until_complete(server.serve())
