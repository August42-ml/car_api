from sqlalchemy.orm import Session

from infrastructure.database.base import SessionLocal
from infrastructure.database.models.consumable import Consumable
from core.consumable.entities import ConsumableModel

class ConsumableRepository:
    
    def __init__(self, session: Session):
        self.session = session

    def add(self, consumable: ConsumableModel) -> None:
        self.session.add(Consumable(
            name=consumable.name,
            last=consumable.last,
            delta=consumable.delta,
            next=consumable.next,
        ))
        self.session.commit()

    def get(self, name: str) -> Consumable:
        return self.session.query(Consumable).filter(Consumable.name==name).first()
    
    def update(self, name: str, consumable: ConsumableModel) -> None:
        current_consumable = self.session.query(Consumable).filter(Consumable.name==name).first()
        current_consumable.name = consumable.name
        current_consumable.last = consumable.last
        current_consumable.delta = consumable.delta
        current_consumable.next = consumable.next
        self.session.commit()

    def delete(self, name: str) -> None:
        current_consumable = self.session.query(Consumable).filter(Consumable.name==name).first()
        self.session.delete(current_consumable)
        self.session.commit()

consumable_repository = ConsumableRepository(SessionLocal())