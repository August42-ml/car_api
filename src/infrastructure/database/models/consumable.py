from sqlalchemy import Column, Integer, String, ForeignKey

from infrastructure.database.base import Base

class Consumable(Base):
    __tablename__ = "consumable"

    id = Column(Integer, primary_key=True)
    car_id = Column(ForeignKey("car.id"))
    name = Column(String, unique=True, nullable=False)
    last = Column(Integer, nullable=False)
    delta = Column(Integer, nullable=False)
    next = Column(Integer, nullable=False)