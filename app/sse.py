import asyncio

from .singleton import Singleton


class SSEvent(asyncio.Event, Singleton):
    def __init__(self):
        super().__init__()
        self.data = None

    def send(self, data):
        self.data = data
        self.set()
        self.clear()
