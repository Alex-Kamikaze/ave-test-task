from pydantic import BaseModel

class AddressResponse(BaseModel):
    """
    Ответ API, содержащий адрес и телефон

    Attributes:
        address (str): Адрес
    """
    address: str