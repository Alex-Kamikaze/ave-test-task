from app.tests.redis_factory import AddressPhoneDataFactory

def test_repo_insertion(mock_repository):
    data = AddressPhoneDataFactory()
    mock_repository.upsert_phone_address_info(data)
    retrieved_address = mock_repository.get_address_by_phone(data.phone)
    assert retrieved_address == data.address

def test_repo_retrieval_nonexistent_phone(mock_repository):
    non_existent_phone = "000-000-0000"
    retrieved_address = mock_repository.get_address_by_phone(non_existent_phone)
    assert retrieved_address is None

def test_repo_check_phone_exists(mock_repository):
    data = AddressPhoneDataFactory()
    mock_repository.upsert_phone_address_info(data)
    assert mock_repository.check_phone_exists(data.phone) is True
    assert mock_repository.check_phone_exists("000-000-0000") is False

def test_repo_update_data(mock_repository):
    data = AddressPhoneDataFactory()
    mock_repository.upsert_phone_address_info(data)
    new_address = "123 New St, New City, NC"
    data.address = new_address
    mock_repository.upsert_phone_address_info(data)
    retrieved_address = mock_repository.get_address_by_phone(data.phone)
    assert retrieved_address == new_address

def test_repo_deletion(mock_repository):
    data = AddressPhoneDataFactory()
    mock_repository.upsert_phone_address_info(data)
    mock_repository.delete_phone_address_info(data.phone)
    retrieved_address = mock_repository.get_address_by_phone(data.phone)
    assert retrieved_address is None

def test_repo_deletion_nonexistent_phone(mock_repository):
    non_existent_phone = "000-000-0000"
    mock_repository.delete_phone_address_info(non_existent_phone)

