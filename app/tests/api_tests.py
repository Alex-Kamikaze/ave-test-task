from main import app
from fastapi.testclient import TestClient
from app.tests.redis_factory import AddressPhoneDataFactory

def test_healthcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_incorrect_number_is_sent(api_client):
    data = {
        "phone": "invalid-phone-number",
        "address": "Some Address"
    }
    response = api_client.put("/api/insert", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Неверный формат номера телефона"}

    
    response = api_client.get("/api/get/invalid")
    assert response.status_code == 400
    assert response.json() == {"detail": "Неверный формат номера телефона"}

    response = api_client.post("/api/update", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Неверный формат номера телефона"}

    response = api_client.delete("/api/delete/invalid")
    assert response.status_code == 400
    assert response.json() == {"detail": "Неверный формат номера телефона"}

def test_phone_retrieval(api_client):
    data = AddressPhoneDataFactory().model_dump()
    response = api_client.put("/api/insert", json=data)
    print(response.json())
    assert response.status_code == 200
    response = api_client.get(f"/api/get/{data['phone']}")
    assert response.status_code == 200
    assert response.json() == {"address": data["address"]}

def test_phone_retrieval_not_found(api_client):
    response = api_client.get("/api/get/+79520302751")
    assert response.status_code == 404
    assert response.json() == {"detail": "Номер телефона не найден"}

def test_phone_insertion(api_client):
    data = AddressPhoneDataFactory().model_dump()
    response = api_client.put("/api/insert", json=data)
    assert response.status_code == 200
    assert response.json() == {"detail": "Вставка успешна"}

def test_phone_insertion_existing(api_client):
    data = AddressPhoneDataFactory().model_dump()
    api_client.put("/api/insert", json=data)
    response = api_client.put("/api/insert", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": "Номер телефона уже существует"}

def test_phone_update(api_client):
    data = AddressPhoneDataFactory().model_dump()
    api_client.put("/api/insert", json=data)
    new_address = "123 New St, New City, NC"
    data["address"] = new_address
    response = api_client.post("/api/update", json=data)
    assert response.status_code == 200
    assert response.json() == {"detail": "Обновление успешно"}
    get_response = api_client.get(f"/api/get/{data['phone']}")
    assert get_response.json() == {"address": new_address}

def test_update_nonexistent_phone(api_client):
    data = AddressPhoneDataFactory().model_dump()
    response = api_client.post("/api/update", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Номер телефона не найден"}

def test_delete_phone(api_client):
    data = AddressPhoneDataFactory().model_dump()
    api_client.put("/api/insert", json=data)
    response = api_client.delete(f"/api/delete/{data['phone']}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Удаление успешно"}
    get_response = api_client.get(f"/api/get/{data['phone']}")
    assert get_response.status_code == 404

def test_delete_nonexistent_phone(api_client):
    response = api_client.delete("/api/delete/+79520302751")
    assert response.status_code == 404
    assert response.json() == {"detail": "Номер телефона не найден"}