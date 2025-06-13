from .exception import CarDoesNotExistError, CarAlreadyExistsError
from .schemas import Car


class CarManager:

    def __init__(self):
        self.cars = {}

    def get(self, car_id: int) -> dict:
        if car_id not in self.cars:
            raise CarDoesNotExistError("Car doesnt exist in storage")
        return self.cars.get(car_id)

    def add(self, car: Car) -> None:
        if car.id in self.cars:
            raise CarAlreadyExistsError("Car is already in storage")
        self.cars.update({car.id: car})

    def update(self, car_id: int, car: Car) -> None:
        if car_id not in self.cars:
            raise CarDoesNotExistError("Car doesnt exist in storage")
        self.cars.update({car_id: car})

    def delete(self, car_id: int) -> None:
        if car_id not in self.cars:
            raise CarDoesNotExistError("Car doesnt exist in storage")
        del self.cars[car_id]

car_manager = CarManager()