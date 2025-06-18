from fastapi import HTTPException, status
from functools import wraps

from core.consumable.exceptions import ConsumableAlreadyExists, ConsumableDoesntExists
from core.cars.exception import CarDoesNotExistError

def consumable_decorator_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConsumableAlreadyExists, ConsumableDoesntExists, CarDoesNotExistError) as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return wrapper
