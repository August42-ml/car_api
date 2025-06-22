from sqlalchemy.orm import Session

from infrastructure.database.base import SessionLocal
from infrastructure.database.models.consumable import Consumable
from core.consumable.entities import ConsumableModel

class ConsumableRepository:
    
    def __init__(self, session: Session):
        self.session = session

    def add(self, consumable: ConsumableModel, car_id: int) -> None:
        self.session.add(Consumable(id=consumable.id,
                                    car_id=car_id,
                                    name=consumable.name,
                                    last=consumable.last,
                                    delta=consumable.delta,
                                    next=consumable.next,
                                    ))
        self.session.commit()

    def get(self, id: int) -> Consumable:
        return self.session.query(Consumable).filter(Consumable.id==id).first()
    
    def update(self, id: int, consumable: ConsumableModel, car_id: int) -> None:
        current_consumable = self.get(id)

        self.session.add(current_consumable)
        current_consumable.car_id = car_id
        current_consumable.name = consumable.name
        current_consumable.last = consumable.last
        current_consumable.delta = consumable.delta
        current_consumable.next = consumable.next
        self.session.commit()

    def delete(self, id: int) -> None:
        current_consumable = self.get(id)
        self.session.delete(current_consumable)
        self.session.commit()

consumable_repository = ConsumableRepository(SessionLocal())