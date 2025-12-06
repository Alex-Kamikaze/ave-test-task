import factory
from app.storage.models import AddressPhoneData

class AddressPhoneDataFactory(factory.Factory):
    class Meta:
        model = AddressPhoneData

    phone = "+79817390409"
    address = factory.Faker('address')