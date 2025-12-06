import pytest
from pytest_mock_resources import create_redis_fixture
from app.repository.repo import Repository
from app.services.storage_service import StorageService
from app.api.deps.repository_dependency import provide_storage_service
from main import app
from fastapi.testclient import TestClient

mock_redis = create_redis_fixture()

@pytest.fixture
def redis_url(mock_redis) -> str:
    """
    Создает мок URL для подключения к мокированному Redis
    """
    conn = mock_redis.connection_pool.connection_kwargs
    host = conn.get("host", "localhost")
    port = conn.get("port", 6379)
    db = conn.get("db", 0)
    password = conn.get("password")
    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    return f"redis://{host}:{port}/{db}"

@pytest.fixture
def mock_repository(redis_url):
    """
    Создает мок репозиторий с использованием мокированного Redis
    """

    return Repository(redis_url=redis_url)

@pytest.fixture
def mock_storage_service(mock_repository):
    """
    Создает мок сервис хранилища с использованием мокированного репозитория
    """

    return StorageService(repository=mock_repository)

@pytest.fixture()
def api_client(mock_storage_service):

    app.dependency_overrides[provide_storage_service] = lambda: mock_storage_service
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()