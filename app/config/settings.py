from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import RedisDsn

class Settings(BaseSettings):
    """
    Конфиг приложения, который подтягивается из env-файла

    Attributes:
        redis_url (RedisDsn): URL для подключения к Redis (по умолчанию redis://localhost:6379/0)
        host (str): Хост для запуска FastAPI (по умолчанию 0.0.0.0)
        port (int): Порт для запуска FastAPI (по умолчанию 8000)
        debug (bool): Режим отладки (по умолчанию True)
    """
    redis_url: RedisDsn = "redis://localhost:6379/0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
