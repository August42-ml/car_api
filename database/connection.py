from sqlmodel import SQLModel, Session, create_engine
from models.car import Car

database_file = "car.db"
database_conncetion_string = f"sqlite:///{database_file}"
connect_args = {"check_same_thread": False}
engine_url = create_engine(database_conncetion_string, connect_args=connect_args, echo=True)

def connect():
    SQLModel.metadata.create_all(engine_url)

def get_session():
    with Session(engine_url) as session:
        yield session