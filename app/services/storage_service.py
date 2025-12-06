from app.repository.repo import Repository, repository_instance
from app.storage.models import AddressPhoneData
from app.exceptions.repository_exceptions import (
    PhoneNotFoundException,
    InsertionFailedException,
    UpdateFailedException,
    DeletionFailedException,
    AddressAlreadyExistsException,
)


class StorageService:
    """
    Use-case слой для взаимодействия с хранилищем Redis

    Attributes:
        repository (Repository): Экземпляр репозитория для взаимодействия с Redis
    """

    def __init__(self, repository: Repository = repository_instance):
        self.repository = repository

    def get_address_by_phone(self, phone: str) -> str:
        """
        Возвращает адрес по номеру телефона

        Args:
            phone (str): Номер телефона

        Returns:
            out (str): Адрес, связанный с номером телефона

        Raises:
            PhoneNotFoundException: Если номер телефона не найден в хранилище
        """

        phone = self.repository.get_address_by_phone(phone)
        if not phone:
            raise PhoneNotFoundException()

        return phone
    
    def insert_phone_address_info(self, data: AddressPhoneData):
        """
        Вставляет связку адрес-телефон в хранилище Redis

        Args:
            data (AddressPhoneData): Данные адрес-телефон для вставки

        Raises:
            AddressAlreadyExistsException: Если связка с таким телефоном уже существует
            InsertionFailedException: Если вставка данных не удалась
        """

        if self.repository.check_phone_exists(data.phone):
            raise AddressAlreadyExistsException()
        try:
            self.repository.upsert_phone_address_info(data)
        except Exception:
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

        if not self.repository.check_phone_exists(data.phone):
            raise PhoneNotFoundException()
        try:
            self.repository.upsert_phone_address_info(data)
        except Exception:
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

        if not self.repository.check_phone_exists(phone):
            raise PhoneNotFoundException()
        try:
            self.repository.delete_phone_address_info(phone)
        except Exception:
            raise DeletionFailedException()