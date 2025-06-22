from infrastructure.database.repositories.consumable import consumable_repository, ConsumableRepository
from .entities import ConsumableModel
from api.rest.consumable.schemas import ConsumableSchema
from core.cars.services import car_service
from .exceptions import ConsumableAlreadyExists, ConsumableDoesntExists

class ConsumableService:
    def __init__(self, repository: ConsumableRepository):
        self.repository = repository

    def get(self, id: int) -> ConsumableSchema:
        try:
            consumable = self.repository.get(id) 
            return ConsumableSchema(name=consumable.name,
                                    last=consumable.last,
                                    delta=consumable.delta,
                                    next=consumable.next,
                                    )
        except:
            raise ConsumableDoesntExists("Consumable isn't in a storage")

    def add(self, consumable: ConsumableSchema, car_id: int) -> None:
        if self.get(consumable.id):
            raise ConsumableAlreadyExists("Consumable is in a storage")
        
        car = car_service.get(car_id)

        next = consumable.last + consumable.delta
        consumable = dict(consumable)
        consumable.update({"next": next})

        self.repository.add(ConsumableModel(**consumable), car_id=car.id,)
        
    def update(self, id: int, consumable: ConsumableSchema, car_id: int) -> None:
        if not self.get(consumable.id):
            raise ConsumableDoesntExists("Consumable isn't in a storage")
        
        car = car_service.get(car_id)

        next = consumable.last + consumable.delta
        consumable = dict(consumable)
        consumable.update({"next": next}) 

        self.repository.update(id, ConsumableModel(**consumable), car_id=car.id)

    def check(self, id: int) -> str:
        consumable = self.repository.get(id)
        car = car_service.get(consumable.car_id)

        delta = consumable.next - car.mileage
        if delta > 0: 
            return f"{consumable.name} is fine. {delta} mileage left"
        return f"{abs(delta)} with non-replaced {consumable.name}"
    
    def delete(self, id: int) -> None:
        if not self.get(id):
            raise ConsumableDoesntExists("Consumable isn't in a storage")
        self.repository.delete(id)


consumable_service = ConsumableService(consumable_repository)