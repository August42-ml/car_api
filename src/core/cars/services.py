from infrastructure.database.repositories.car import car_repository, CarRepository
from api.rest.cars.schemas import CarSchema
from core.cars.exception import CarAlreadyExistsError, CarDoesNotExistError
from .entities import CarModel

class CarService:

    def __init__(self, repository: CarRepository) -> None:
        self.repository = repository

    def get(self, name: str) -> CarSchema:
        try:
            car = self.repository.get(name)
            return CarSchema(name=car.name, mileage=car.mileage)
        except:
            raise CarDoesNotExistError("Car isn't in a storage")
    
    def add(self, car: CarSchema) -> None:
        try:
            self.repository.add(CarModel(
                                **dict(car)
                            ))
        except:
            raise CarAlreadyExistsError("Car already exists")

    def update(self, name: str, car: CarSchema) -> None:
        try:
            self.repository.update(name,
                                CarModel(**dict(car)
                                ))
        except:
            raise CarDoesNotExistError("Car isn't in a storage")
        

    def delete(self, name: str) -> None:
        try:
            self.repository.delete(name)
        except:
            raise CarDoesNotExistError("Car isn't in a storage")

car_service = CarService(repository=car_repository)