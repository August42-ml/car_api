from infrastructure.database.repositories.consumable import consumable_repository, ConsumableRepository
from .entities import ConsumableModel
from api.rest.consumable.schemas import ConsumableSchema
from core.cars.services import car_service
from .exceptions import ConsumableAlreadyExists, ConsumableDoesntExists

class ConsumableService:
    def __init__(self, repository: ConsumableRepository):
        self.repository = repository

    def get(self, name: str) -> ConsumableSchema:
        try:
            consumable = self.repository.get(name) 
            return ConsumableSchema(name=consumable.name,
                                    last=consumable.last,
                                    delta=consumable.delta,
                                    next=consumable.next,
                                    )
        except:
            raise ConsumableDoesntExists("Consumable isn't in a storage")

    def add(self, consumable: ConsumableSchema) -> None:
        next = consumable.last + consumable.delta
        consumable = dict(consumable)
        consumable.update({"next": next})
        try:
            self.repository.add(
                ConsumableModel(**consumable)
                )
        except:
            raise ConsumableAlreadyExists("Consumable is in a storage")
        
    def update(self, name: str, consumable: ConsumableSchema) -> None:
        next = consumable.last + consumable.delta
        consumable = dict(consumable)
        consumable.update({"next": next})
        try:
            self.repository.update(name,
                                ConsumableModel(**consumable)
                                )
        except:
            raise ConsumableDoesntExists("Consumable isn't in a storage")

    def check(self, consumable_name: str, car_name: str) -> str:
        car = car_service.get(car_name)
        consumable = self.get(consumable_name)
        delta = consumable.next - car.mileage

        if delta > 0: 
            return f"{consumable_name} is fine. {delta} mileage left"
        return f"{abs(delta)} with non-replaced {consumable_name}"
    
    def delete(self, name: str) -> None:
        try:
            self.repository.delete(name)
        except:
            raise ConsumableDoesntExists("Consumable isn't in a storage")


consumable_service = ConsumableService(consumable_repository)