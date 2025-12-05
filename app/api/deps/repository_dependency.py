from app.repository.repo import repository_instance, Repository

def provide_repository() -> Repository:
    """
    Провайдер зависимости для репозитория

    Returns:
        Repository: Экземпляр репозитория
    """
    return repository_instance
