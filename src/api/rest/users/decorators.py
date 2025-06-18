from fastapi import HTTPException, Depends, status
from functools import wraps

from .dependencies import get_current_user
from core.users.exceptions import UserAlreadyExistsError, UserDoesntExistError, UserPasswordError

def role_required(func):
    
    @wraps(func)
    def wrapper(*args, current_user = Depends(get_current_user), **kwargs):
        if not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must be admin to do this")
        return func(*args, current_user=current_user, **kwargs)
    return wrapper

def user_exceptions(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (UserPasswordError, UserDoesntExistError, UserAlreadyExistsError) as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    return wrapper
        