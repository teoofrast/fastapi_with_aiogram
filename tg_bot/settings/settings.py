import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    FASTAPI_URL: str
    BASE_NGROK_URL: str


class BotSettings(Settings):

    model_config = SettingsConfigDict(
        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.env'),
        extra='allow'
    )
