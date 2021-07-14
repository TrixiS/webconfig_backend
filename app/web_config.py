import typing

from pydantic import BaseModel, Field

# TODO: create schema file
#       in flask app
#       and take it from static as /config_schema.json


class Config(BaseModel):
    bot_token: str = Field(None, title="Токен бота")
    command_prefix: str = Field("!", title="Префикс команд")
    test_int: int = Field(None, title="Тестовый инт")
    test_float: float = Field(None, title="Тестовый флоат")
    some_list: typing.List[str] = Field([], title="Тестовый список")
    some_dict: typing.Dict[str, str] = Field({}, title="Тестовый дикт")


class Phrases(BaseModel):
    bot_started: str = Field(
        "Бот {bot.user} успешно запущен",
        description="Системная фраза. Пишется в терминал при запуске",
    )


class WebConfig(BaseModel):
    config: Config = Field(Config(), title="Конфиг")
    phrases: Phrases = Field(Phrases(), title="Фразы")
