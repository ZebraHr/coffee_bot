import pytz
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot_app.core.constants import Timezone

TIMEZONE = pytz.timezone(Timezone.TIMEZONE_MOSCOW)


class Settings(BaseSettings):
    """Application settings class."""
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str
    database_url: str
    gen_admin_id: int


settings = Settings()
bot = Bot(settings.bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
