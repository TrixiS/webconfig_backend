import json

from pathlib import Path

import aiofiles

from pydantic import BaseModel, Field

config_path = Path(__file__).parent / "../config.json"


class Config(BaseModel):
    bot_token: str = Field(None, title="Токен бота")
    command_prefix: str = Field("!", title="Префикс команд")


class Phrases(BaseModel):
    bot_started: str = Field(
        "Бот {bot.user} успешно запущен",
        description="Системная фраза. Пишется в терминал при запуске",
    )


class WebConfig(BaseModel):
    config: Config = Field(Config(), title="Конфиг")
    phrases: Phrases = Field(Phrases(), title="Фразы")


async def load_config() -> WebConfig:
    async with aiofiles.open(config_path, "r", encoding="utf-8") as f:
        try:
            json_content = json.loads(await f.read())
        except json.JSONDecodeError:
            json_content = {}

    return WebConfig.parse_obj(json_content)


async def save_config(web_config: WebConfig):
    async with aiofiles.open(config_path, "w", encoding="utf-8") as f:
        await f.write(web_config.json())
