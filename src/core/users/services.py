from bcrypt import hashpw, checkpw, gensalt
from datetime import timedelta, datetime, timezone
from jose import jwt

from api.rest.users.schemas import UserSchema
from infrastructure.database.repositories.user import user_repository_factory
from infrastructure.database.uow import unit_of_work
from infrastructure.database.exceptions import UnitOfWorkError
from .entities import BaseUser
from .exceptions import UserPasswordError, TokenIsInvalid, UserAlreadyExistsError, ServiceError

SECRET_KEY = "121213"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 10


class UserService:
    def __init__(self):
        self.repository_factory = user_repository_factory

    @staticmethod
    def hash_password(password: str) -> str:
        return hashpw(password.encode(), gensalt()).decode()

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return checkpw(password.encode(), hashed_password.encode())

    def add(self, user: UserSchema) -> None:
        try:
            with unit_of_work() as uow:
                user_repository = self.repository_factory(uow.session)

                hashed_password = self.hash_password(user.password)

                if user_repository.get(user.username):
                    raise UserAlreadyExistsError("User has already registered")

                new_user = BaseUser(username=user.username,
                                        email=user.email,
                                        password=hashed_password,
                                        is_admin=user.is_admin)
                
                user_repository.add(new_user)
        except UnitOfWorkError as error:
            raise ServiceError("Failed to add user")


    def get_all(self) -> list[BaseUser]:
        try:
            with unit_of_work() as uow:
                user_repository = self.repository_factory(uow.session)
                return user_repository.get_all()
        except UnitOfWorkError as error:
            raise ServiceError("Failed to get all users")
    
    def login(self, username: str, password: str) -> None:
        try:
            with unit_of_work() as uow:
                user_repository = self.repository_factory(uow.session)

                user = user_repository.get(username)
                if not self.check_password(password, user.password):
                    raise UserPasswordError("Wrong password")
        except UnitOfWorkError as error:
            raise ServiceError("Failed to login")
        
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
        try:
            with unit_of_work() as uow:
                user_repository = self.repository_factory(uow.session) 

                username = self.verify_token(token=token, token_type="access")
                user = user_repository.get(username)
                return BaseUser(id=user.id, 
                                username=user.username,
                                email=user.email,
                                password=user.password,
                                is_admin=user.is_admin,
                                )
        except UnitOfWorkError as error:
            raise ServiceError("Failed to get current user")
        
    @staticmethod
    def verify_token(token_type: str, token: str) -> str:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        if token_type != payload.get("type"):
            raise TokenIsInvalid("Token is invalid")
        return payload.get("sub")
    
    def delete(self, username: str) -> None:
        try:
            with unit_of_work() as uow:
                user_repository = self.repository_factory(uow.session) 
                user_repository.delete(username)
        except UnitOfWorkError as error:
            raise ServiceError("Failed to delete user")

    
user_service = UserService()
        
