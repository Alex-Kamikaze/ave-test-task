import pytest
from app.tests.redis_factory import AddressPhoneDataFactory
from app.exceptions.repository_exceptions import PhoneNotFoundException, AddressAlreadyExistsException

def test_service_retriving_phone(mock_storage_service):
    data = AddressPhoneDataFactory()
    mock_storage_service.insert_phone_address_info(data)
    retrieved_address = mock_storage_service.get_address_by_phone(data.phone)
    assert retrieved_address == data.address

def test_service_retriving_nonexistent_phone(mock_storage_service):
    non_existent_phone = "+79520302751"
    with pytest.raises(PhoneNotFoundException):
        mock_storage_service.get_address_by_phone(non_existent_phone)

def test_service_insertion(mock_storage_service):
    data = AddressPhoneDataFactory()
    mock_storage_service.insert_phone_address_info(data)
    retrieved_address = mock_storage_service.get_address_by_phone(data.phone)
    assert retrieved_address == data.address

def test_service_insertion_existing_phone(mock_storage_service):
    data = AddressPhoneDataFactory()
    mock_storage_service.insert_phone_address_info(data)
    with pytest.raises(AddressAlreadyExistsException):
        mock_storage_service.insert_phone_address_info(data)

def test_service_update(mock_storage_service):
    data = AddressPhoneDataFactory()
    mock_storage_service.insert_phone_address_info(data)
    new_address = "123 New St, New City, NC"
    data.address = new_address
    mock_storage_service.update_phone_address_info(data)
    retrieved_address = mock_storage_service.get_address_by_phone(data.phone)
    assert retrieved_address == new_address

def test_service_update_nonexistent_phone(mock_storage_service):
    data = AddressPhoneDataFactory()
    with pytest.raises(PhoneNotFoundException):
        mock_storage_service.update_phone_address_info(data)

def test_service_deletion(mock_storage_service):
    data = AddressPhoneDataFactory()
    mock_storage_service.insert_phone_address_info(data)
    mock_storage_service.delete_phone_address_info(data.phone)
    with pytest.raises(PhoneNotFoundException):
        mock_storage_service.get_address_by_phone(data.phone)

def test_service_deletion_nonexistent_phone(mock_storage_service):
    non_existent_phone = "+79520302751"
    with pytest.raises(PhoneNotFoundException):
        mock_storage_service.delete_phone_address_info(non_existent_phone)