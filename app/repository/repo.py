from redis import Redis
from app.config.settings import settings
from app.storage.models import AddressPhoneData


class Repository:
    """
    Основной класс для вазаимодействия с хранилищем Redis

    Attributes:
        redis (Redis): Клиент Redis
    """

    def __init__(self, redis_url: str = str(settings.redis_url)):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    def get_address_by_phone(self, phone: str) -> str:
        """
        Возвращает адрес по номеру телефона из хранилища Redis

        Args:
            phone (str): Номер телефона

        Returns:
            out (str): Адрес, связанный с номером телефона
        """
        return self.redis.get(phone)
    

    def check_phone_exists(self, phone: str) -> bool:
        """
        Проверяет существование номера телефона в хранилище Redis

        Args:
            phone (str): Номер телефона для проверки

        Returns:
            out (bool): True, если номер телефона существует, иначе False
        """
        return self.redis.exists(phone) == 1

    def upsert_phone_address_info(self, data: AddressPhoneData):
        """
        Вставляет или обновляет связку адрес-телефон в хранилище Redis

        Args:
            data (AddressPhoneData): Данные адрес-телефон для вставки
        """
        self.redis.set(data.phone, data.address)

    def delete_phone_address_info(self, phone: str):
        """
        Удаляет связку адрес-телефон из хранилища Redis по номеру телефона
        Args:
            phone (str): Номер телефона для удаления
        """
        self.redis.delete(phone)
        
    def __del__(self):
        self.redis.close()

repository_instance = Repository()