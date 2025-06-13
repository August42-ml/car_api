from .manager import CarManager, car_manager
from .schemas import Car

class CarService:

    def __init__(self, manager: CarManager) -> None:
        self.manager = manager

    def get(self, car_id: int) -> dict:
        return self.manager.get(car_id)
    
    def add(self, car: Car) -> None:
        self.manager.add(car)

    def update(self, car_id: int, car: Car) -> None:
        self.manager.update(car_id, car)

    def delete(self, car_id: int) -> None:
        self.manager.delete(car_id)

car_service = CarService(manager=car_manager)