from bcrypt import hashpw, checkpw, gensalt
from datetime import timedelta, datetime, timezone
from jose import jwt

from api.rest.users.schemas import User
from infrastructure.database.repositories.user import user_repository, UserRepository
from .entities import BaseUser
from .exceptions import UserPasswordError, TokenIsInvalid, UserAlreadyExistsError, UserDoesntExistError

SECRET_KEY = "121213"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 10


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    def hash_password(password: str) -> str:
        return hashpw(password.encode(), gensalt()).decode()

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode(), hashed_password.encode())

    def add(self, user: User) -> None:
        hashed_password = self.hash_password(user.password)
        try:
            new_user = BaseUser(username=user.username,
                                email=user.email,
                                password=hashed_password,
                                is_admin=user.is_admin)
            self.repository.add(new_user)
        except:
            raise UserAlreadyExistsError("User was already registered")

    def get_all(self) -> list[BaseUser]:
        return user_repository.get_all()
    
    def login(self, username: str, password: str) -> None:
        user = user_repository.get(username)
        if not self.check_password(password, user.password):
            raise UserPasswordError("Wrong password")
        
    #дублирование
    def create_token(self, username: str, token_type: str) -> str:
        if token_type == "access":
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            payload = {"sub": username, "type": "access", "exp": expire}
            return jwt.encode(payload, SECRET_KEY, ALGORITHM)
        
        if token_type == "refresh":
            expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            payload = {"sub": username, "type": "refresh", "exp": expire}
            return jwt.encode(payload, SECRET_KEY, ALGORITHM)

    def get_current_user(self, token: str) -> BaseUser:        
        username = self.verify_token(token=token, token_type="access")
        return user_repository.get(username)
    
    @staticmethod
    def verify_token(token_type: str, token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        if token_type != payload.get("type"):
            raise TokenIsInvalid("Token is invalid")
        return payload.get("sub")
    
    def delete(self, username: str) -> None:
        try:
            self.repository.delete(username)
        except:
            raise UserDoesntExistError("User isn't in a storage")

    
user_service = UserService(user_repository)
        
