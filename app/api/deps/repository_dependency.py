from app.services.storage_service import StorageService
from app.repository.repo import repository_instance, Repository

def provide_repository() -> Repository:
    """
    Провайдер зависимости для репозитория

    Returns:
        Repository: Экземпляр репозитория
    """
    return repository_instance

def provide_storage_service() -> StorageService:
    """
    Провайдер зависимости для сервиса хранилища

    Returns:
        StorageService: Экземпляр сервиса хранилища
    """
    return StorageService(repository=provide_repository())