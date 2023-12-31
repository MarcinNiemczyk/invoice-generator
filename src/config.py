import logging

from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


config = Config()
if not config.SECRET_KEY:
    log.warning("No JWT Secret specified. Authentication system is suppressed.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
