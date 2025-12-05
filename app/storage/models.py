from pydantic import BaseModel

class AddressPhoneData(BaseModel):
    """
    Связка адрес-телефон в хранилище Redis

    Attributes:
        address (str): Адрес
        phone (str): Телефон
    """
    address: str
    phone: str