from .exceptions import UserAlreadyExistsError, UserDoesntExistError
from .models import BaseUser

class UserManger:
    
    def __init__(self):
        self.users = {}

    def add(self, user: BaseUser) -> None:
        if user.username in self.users:
            raise UserAlreadyExistsError("User is already in a storage")
        self.users.update({user.username: user})

    def get(self, username: str) -> BaseUser:
        if username not in self.users:
            raise UserDoesntExistError("User isn't in a storage")
        return self.users.get(username)
    
    def get_all(self) -> list[BaseUser]:
        return [user for user in self.users.values()]
    
user_manager = UserManger()