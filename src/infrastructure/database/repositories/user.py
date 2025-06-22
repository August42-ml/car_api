from sqlalchemy.orm import Session

from core.users.entities import BaseUser
from infrastructure.database.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, username: str) -> User:
        return self.session.query(User).filter(User.username==username).first()
    
    def get_all(self) -> list[User]:
        return self.session.query(User).all()
    
    def delete(self, username: str) -> None:
        user = self.session.query(User).filter(User.username==username).first()
        self.session.delete(user)

    def add(self, user: BaseUser) -> None:
        self.session.add(User(
            email=user.email,
            username=user.username,
            password=user.password,
            is_admin=user.is_admin,
        ))


def user_repository_factory(session: Session) -> UserRepository:
    return UserRepository(session) 
