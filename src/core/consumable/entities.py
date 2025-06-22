from typing import Optional

class ConsumableModel:

    def __init__(self, name: str, last: int, delta: int, next: int, id: Optional[int] = None):
        self.id = id
        self.name = name 
        self.last = last
        self.delta = delta
        self.next = next

    def get_info(self) -> dict:
        return {
                "id": self.id,
                "name": self.name,
                "price": self.last,
                "quantity": self.next
                }