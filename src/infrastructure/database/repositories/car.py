from sqlalchemy.orm import Session

from infrastructure.database.models.car import Car
from core.cars.entities import CarModel
from infrastructure.database.base import SessionLocal

class CarRepository:
    
    def __init__(self, session: Session):
        self.session = session

    def get(self, name: str) -> Car:
        return self.session.query(Car).filter(Car.name==name).first()
    
    def add(self, car: CarModel) -> None:
        self.session.add(Car(
            name=car.name,
            mileage=car.mileage
        ))
        self.session.commit()
    
    def update(self, name: str, car: CarModel) -> None:
        current_car = self.session.query(Car).filter(Car.name==name).first()
        current_car.name = car.name
        current_car.mileage = car.mileage
        self.session.commit()

    def delete(self, name: str) -> None:
        car = self.session.query(Car).filter(Car.name==name).first()
        self.session.delete(car)
        self.session.commit()

car_repository = CarRepository(SessionLocal())