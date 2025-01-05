"""Модуль для настройки конфигурации бота и FastAPI."""

# STDLIB
import os

# THIRDPARTY
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки для бота и FastAPI.

    Этот класс наследуется от `pydantic.BaseSettings` и
    содержит конфигурационные параметры для бота,
    а также для FastAPI и внешних сервисов.

    Атрибуты:
        TG_BOT_TOKEN (str): Токен для Telegram-бота.
        FASTAPI_URL (str): URL для подключения к FastAPI.
        BASE_NGROK_URL (str): Основной URL для ngrok.

    Описание:
        - Параметры настраиваются через переменные окружения или файл `.env`.
    """

    TG_BOT_TOKEN: str
    FASTAPI_URL: str
    BASE_NGROK_URL: str


class BotSettings(Settings):
    """Конфигурация настроек для бота.

    Этот класс наследуется от `pydantic_settings.Settings` и предоставляет
    конфигурационные опции для бота, включая загрузку переменных окружения
    и разрешение дополнительных полей в настройках.

    Атрибуты:
        model_config (SettingsConfigDict): Словарь конфигурации
        для настроек, указывающий местоположение файла окружения
        и разрешающий дополнительные поля.

    Конфигурация:
        - Файл окружения расположен на два уровня выше текущего файла.
        - Разрешение дополнительных полей в настройках установлено
        флагом `extra='allow'`.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            '.env',
        ),
        extra='allow',
    )
