from fastapi import HTTPException, status
from functools import wraps

from core.cars.exception import CarAlreadyExistsError, CarDoesNotExistError

def car_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (CarDoesNotExistError, CarAlreadyExistsError) as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return wrapper
        