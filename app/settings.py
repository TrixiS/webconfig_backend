from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):

    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    APP_PORT: int = 5000


settings = Settings()