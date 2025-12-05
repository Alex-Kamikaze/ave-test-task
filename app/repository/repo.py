from redis import Redis
from app.core.settings import settings
from app.storage.models import AddressPhoneData
from app.exceptions.repository_exceptions import (
    PhoneNotFoundException,
    InsertionFailedException,
    UpdateFailedException,
    DeletionFailedException,
    AddressAlreadyExistsException
)


class Repository:
    """
    Основной класс для вазаимодействия с хранилищем Redis

    Attributes:
        redis (Redis): Клиент Redis
    """

    def __init__(self):
        self.redis = Redis.from_url(str(settings.redis_url), decode_responses=True)

    def get_address_by_phone(self, phone: str) -> str:
        """
        Возвращает адрес по номеру телефона из хранилища Redis

        Args:
            phone (str): Номер телефона

        Returns:
            out (str): Адрес, связанный с номером телефона

        Raises:
            PhoneNotFoundException: Если номер телефона не найден в хранилище
        """
        address = self.redis.get(phone)
        if address is None:
            raise PhoneNotFoundException()
        return address

    def insert_phone_address_info(self, data: AddressPhoneData):
        """
        Вставляет связку адрес-телефон в хранилище Redis
        Args:
            data (AddressPhoneData): Данные адрес-телефон для вставки

        Raises:
            InsertionFailedException: Если вставка данных не удалась
        """
        if self.redis.exists(data.phone):
            raise AddressAlreadyExistsException()
        result = self.redis.set(data.phone, data.address)
        if not result:
            raise InsertionFailedException()

    def update_phone_address_info(self, data: AddressPhoneData):
        """
        Обновляет связку адрес-телефон в хранилище Redis

        Args:
            data (AddressPhoneData): Данные адрес-телефон для обновления

        Raises:
            PhoneNotFoundException: Если номер телефона не найден в хранилище
            UpdateFailedException: Если обновление данных не удалось

        """
        if not self.redis.exists(data.phone):
            raise PhoneNotFoundException()
        result = self.redis.set(data.phone, data.address)
        if not result:
            raise UpdateFailedException()

    def delete_phone_address_info(self, phone: str):
        """
        Удаляет связку адрес-телефон из хранилища Redis по номеру телефона
        Args:
            phone (str): Номер телефона для удаления

        Raises:
            PhoneNotFoundException: Если номер телефона не найден в хранилище
            DeletionFailedException: Если удаление данных не удалось
        """
        if not self.redis.exists(phone):
            raise PhoneNotFoundException()
        result = self.redis.delete(phone)
        if not result:
            raise DeletionFailedException()
        
    def __del__(self):
        self.redis.close()

repository_instance = Repository()
