from infrastructure.database.repositories.car import car_repository, CarRepository
from api.rest.cars.schemas import CarSchema
from core.cars.exception import CarAlreadyExistsError, CarDoesNotExistError
from core.users.entities import BaseUser  
from .entities import CarModel

class CarService:

    def __init__(self, repository: CarRepository) -> CarSchema:
        self.repository = repository

    def get(self, id: str) -> CarSchema:
        try:
            car = self.repository.get_car_by_id(id)
            return CarSchema(id=car.id, name=car.name, mileage=car.mileage)
        except:
            raise CarDoesNotExistError("Car isn't in a storage")
    
    def get_all(self, user_id: id) -> list[CarSchema]:
        cars = self.repository.get_all(user_id)
        
        schemas = []
        for car in cars:
            schemas.append(CarSchema(id=car.id, name=car.name, mileage=car.mileage))
        return schemas

    def add(self, car: CarSchema, user: BaseUser) -> None:
        if self.repository.get_car_by_id(car.id):
            raise CarAlreadyExistsError("Car already exists")
        self.repository.add(CarModel(**dict(car)), user_id=user.id)


    def update(self, id: int, car: CarSchema, user: BaseUser) -> None:
        if not self.repository.get_car_by_id(id):
            raise CarDoesNotExistError("Car isn't in a storage")
        self.repository.update(id, CarModel(**dict(car)), user_id = user.id)
        
    def delete(self, id: int) -> None:
        if not self.repository.get_car_by_id(id):
            raise CarDoesNotExistError("Car isn't in a storage")
        self.repository.delete(id)

car_service = CarService(repository=car_repository)