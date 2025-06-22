from pydantic import BaseModel
from typing import Optional

class ConsumableSchema(BaseModel):
    id: int
    name: str 
    last: int
    delta: int
    next: Optional[int] = None