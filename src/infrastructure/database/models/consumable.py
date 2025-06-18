from sqlalchemy import Column, Integer, String

from infrastructure.database.base import Base

class Consumable(Base):
    __tablename__ = "consumable"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    last = Column(Integer, nullable=False)
    delta = Column(Integer, nullable=False)
    next = Column(Integer, nullable=False)