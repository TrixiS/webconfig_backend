import json

from pathlib import Path
from typing import List

import aiofiles

from pydantic import BaseModel, Field

config_path = Path(__file__).parent / "../config.json"


class Config(BaseModel):
    bot_token: str = Field(None, title="Токен бота")
    command_prefixes: List[str] = Field(["!", "!!"], title="Префиксы команд")


class Phrases(BaseModel):
    bot_started: str = Field("Бот {bot.user} успешно запущен")
    bot: str = Field("Бот")
    bot_start: str = Field("Запустить")
    bot_reload: str = Field("Перезапустить")
    bot_kill: str = Field("Остановить")
    save: str = Field("Сохранить")


class WebConfig(BaseModel):
    _instance: "WebConfig" = None

    config: Config = Field(Config(), title="Конфиг")
    phrases: Phrases = Field(Phrases(), title="Фразы")

    @classmethod
    async def load(cls) -> "WebConfig":
        async with aiofiles.open(config_path, "r", encoding="utf-8") as f:
            try:
                json_content = json.loads(await f.read())
            except json.JSONDecodeError:
                json_content = {}

        return cls.parse_obj(json_content)

    async def save(self):
        async with aiofiles.open(config_path, "w", encoding="utf-8") as f:
            await f.write(self.json())
