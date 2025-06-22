from sqlalchemy import Column, String, Integer, ForeignKey

from infrastructure.database.base import Base

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    name = Column(String, nullable=False)
    mileage = Column(Integer, nullable=False)

