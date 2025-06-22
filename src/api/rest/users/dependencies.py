from fastapi import Depends, HTTPException, status
from jose import JWTError
from fastapi.security import APIKeyHeader

from core.users.services import user_service
from core.users.exceptions import TokenIsInvalid
from core.users.entities import BaseUser

def get_current_user(token: str = Depends(APIKeyHeader(name="auth"))) -> BaseUser:
    try:
        return user_service.get_current_user(token)
    except (JWTError, TokenIsInvalid) as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))

