from pydantic import BaseModel

class AddressResponse(BaseModel):
    """
    Ответ API, содержащий адрес

    Attributes:
        address (str): Адрес
    """
    address: str