from sqlalchemy import Column, String, Integer

from infrastructure.database.base import Base

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mileage = Column(Integer, nullable=False)

