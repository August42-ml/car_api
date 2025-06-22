from sqlalchemy.orm import Session

from infrastructure.database.models.car import Car
from core.cars.entities import CarModel
from infrastructure.database.base import SessionLocal

class CarRepository:
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_car_by_id(self, id: int) -> Car:
        return self.session.query(Car).filter(Car.id==id).first()
    
    def get_all(self, user_id: int) -> list[Car]:
        return self.session.query(Car).filter(Car.user_id==user_id).all()

    def add(self, car: CarModel, user_id: int) -> None:
        self.session.add(Car(id=car.id,
                            name=car.name,  
                            mileage=car.mileage,
                            user_id=user_id
                            )
                        )
        self.session.commit()
    
    def update(self, id: int, car: CarModel, user_id: int) -> None:
        current_car = self.get_car_by_id(id)

        self.session.add(current_car)
        current_car.user_id = user_id
        current_car.name = car.name
        current_car.mileage = car.mileage
        self.session.commit()

    def delete(self, id: int) -> None:
        car = self.get_car_by_id(id)
        self.session.delete(car)
        self.session.commit()

car_repository = CarRepository(SessionLocal())