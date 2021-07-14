import uvicorn

from .app import app
from .settings import settings

uvicorn.run(app, port=settings.APP_PORT)
