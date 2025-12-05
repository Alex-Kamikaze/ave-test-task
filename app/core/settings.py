from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import RedisDsn

class Settings(BaseSettings):
    """
    Конфиг приложения, который подтягивается из env-файла

    Attributes:
        redis_url (RedisDsn): URL для подключения к Redis
        host (str): Хост для запуска FastAPI
        port (int): Порт для запуска FastAPI
        debug (bool): Режим отладки (по умолчанию True)
    """
    redis_url: RedisDsn
    host: str
    port: int
    debug: bool = True
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()