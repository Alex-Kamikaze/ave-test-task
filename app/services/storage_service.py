import phonenumbers
from app.repository.repo import Repository, repository_instance
from app.storage.models import AddressPhoneData
from app.exceptions.repository_exceptions import (
    PhoneNotFoundException,
    InsertionFailedException,
    UpdateFailedException,
    DeletionFailedException,
    AddressAlreadyExistsException,
    PhoneNotValidException
)


class StorageService:
    """
    Use-case слой для взаимодействия с хранилищем Redis

    Attributes:
        repository (Repository): Экземпляр репозитория для взаимодействия с Redis
    """

    def __init__(self, repository: Repository = repository_instance):
        self.repository = repository
    
    def formalize_phone(self, phone: str) -> str:
        """
        Форматирует номер телефона в международный формат

        Args:
            phone (str): Номер телефона для форматирования

        Returns:
            out (str): Форматированный номер телефона

        Raises:
            PhoneNotValidException: Если номер телефона имеет неверный формат
        """

        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise PhoneNotValidException()
            return phonenumbers.format_number(
                parsed_phone, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise PhoneNotValidException()

    def get_address_by_phone(self, phone: str) -> str:
        """
        Возвращает адрес по номеру телефона

        Args:
            phone (str): Номер телефона

        Returns:
            out (str): Адрес, связанный с номером телефона

        Raises:
            PhoneNotFoundException: Если номер телефона не найден в хранилище
            PhoneNotValidException: Если номер телефона имеет неверный формат
        """
        validated_phone = self.formalize_phone(phone)

        result = self.repository.get_address_by_phone(validated_phone)
        if not result:
            raise PhoneNotFoundException()

        return result
    
    def insert_phone_address_info(self, data: AddressPhoneData):
        """
        Вставляет связку адрес-телефон в хранилище Redis

        Args:
            data (AddressPhoneData): Данные адрес-телефон для вставки

        Raises:
            AddressAlreadyExistsException: Если связка с таким телефоном уже существует
            InsertionFailedException: Если вставка данных не удалась
            PhoneNotValidException: Если номер телефона имеет неверный формат
        """
        validated_phone = self.formalize_phone(data.phone)

        if self.repository.check_phone_exists(validated_phone):
            raise AddressAlreadyExistsException()
        try:
            self.repository.upsert_phone_address_info(AddressPhoneData(phone=validated_phone, address=data.address))
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
        validated_phone = self.formalize_phone(data.phone)

        if not self.repository.check_phone_exists(validated_phone):
            raise PhoneNotFoundException()
        try:
            self.repository.upsert_phone_address_info(AddressPhoneData(phone=validated_phone, address=data.address))
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
        validated_phone = self.formalize_phone(phone)

        if not self.repository.check_phone_exists(validated_phone):
            raise PhoneNotFoundException()
        try:
            self.repository.delete_phone_address_info(validated_phone)
        except Exception:
            raise DeletionFailedException()