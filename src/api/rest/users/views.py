from fastapi import APIRouter, Depends

from core.users.services import user_service
from core.users.entities import BaseUser
from .schemas import UserSchema
from .dependencies import get_current_user
from .decorators import role_required, user_exceptions

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/register")
@user_exceptions
def register(user: UserSchema) -> dict:
    user_service.add(user)
    return {"msg": f"User {user.username} was registered successfully"}

@user_router.get("/all")
@role_required
def get_all(current_user=Depends(get_current_user)):
    return user_service.get_all()

@user_router.post("/login")
@user_exceptions
def login(username: str, password: str) -> dict:
    user_service.login(username, password)
    access_token = user_service.create_token(username, "access")
    refresh_token = user_service.create_token(username, "refresh")
    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.get("/ping")
def ping(user: BaseUser = Depends(get_current_user)) -> dict:
    return user.get_info()


@user_router.delete("/{username}")
@role_required
@user_exceptions
def delete_user(username: str, current_user = Depends(get_current_user)) -> dict:
    user_service.delete(username)
    return {"msg": f"{username} was deleted successfully"}