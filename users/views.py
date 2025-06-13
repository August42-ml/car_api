from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from bcrypt import hashpw, gensalt, checkpw
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta

from .exceptions import UserAlreadyExistsError, UserDoesntExistError
from .schemas import User
from .models import BaseUser
from .manager import user_manager

user_router = APIRouter(prefix="/users", tags=["Users"])

SECRET_KEY = "121213"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 20

@user_router.post("/register")
def register(user: User) -> dict:
    hashed_password = hashpw(user.password.encode(), gensalt()).decode("utf-8")
    new_user = BaseUser(username=user.username, email=user.email, password=hashed_password, is_admin=user.is_admin)
    try:
        user_manager.add(new_user)
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return {"msg": f"User {new_user.username} was registered successfully"}

@user_router.get("/all")
def get_all():
    return user_manager.get_all()

@user_router.post("/login")
def login(username: str, password: str) -> dict:
    try:
        current_user = user_manager.get(username)
    except UserDoesntExistError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    
    if checkpw(password.encode(), current_user.password.encode()):
        access_expire_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expire_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        access_payload = {"sub": current_user.username, "type": "access", "exp": access_expire_delta}
        refresh_payload = {"sub": current_user.username, "type": "refresh", "exp": refresh_expire_delta}
        
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": access_token, "refresh_token": refresh_token}
    
@user_router.get("/ping")
def ping(key=Depends(APIKeyHeader(name="auth token"))):
    return {"msg": key}
