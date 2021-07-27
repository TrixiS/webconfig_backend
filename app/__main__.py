from uvicorn import Config, Server

from . import loop
from .app import app
from .settings import settings

config = Config(app, port=settings.APP_PORT, loop=loop)
server = Server(config)

loop.run_until_complete(server.serve())
