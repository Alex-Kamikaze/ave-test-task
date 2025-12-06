class PhoneNotFoundException(Exception):
    """Вызывается, когда телефон не найден в Redis"""
    pass

class InsertionFailedException(Exception):
    """Вызывается, когда вставка данных в Redis не удалась"""
    pass

class UpdateFailedException(Exception):
    """Вызывается, когда обновление данных в Redis не удалось"""
    pass

class DeletionFailedException(Exception): 
    """Вызывается, когда удаление данных из Redis не удалось"""
    pass

class AddressAlreadyExistsException(Exception):
    """Вызывается, когда адрес уже существует в Redis"""
    pass

class PhoneNotValidException(Exception):
    """Вызывается, когда номер телефона имеет неверный формат"""
    pass