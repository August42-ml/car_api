from fastapi import APIRouter, Depends

from core.consumable.services import consumable_service
from api.rest.users.dependencies import get_current_user
from .schemas import ConsumableSchema
from .decorators import consumable_decorator_exception

consumable_router = APIRouter(prefix="/consumables", tags=["Consumables"])

@consumable_router.get("/{id}")
@consumable_decorator_exception
def get_consumable(id: int, 
                current_user = Depends(get_current_user),
) -> ConsumableSchema:
    return consumable_service.get(id)

@consumable_router.post("/add")
@consumable_decorator_exception
def add_consumable(consumable: ConsumableSchema,
                car_id: str,
                current_user = Depends(get_current_user),
) -> dict:
    consumable_service.add(consumable, car_id)
    return {"msg": f"Consumable {consumable.name} was added successfully"}

@consumable_router.put("/{id}")
@consumable_decorator_exception
def update_consumable(id: int,
                    consumable: ConsumableSchema,
                    car_id: str,
                    current_user = Depends(get_current_user),
) -> dict:
    consumable_service.update(id, consumable, car_id)
    return {"msg": f"Consumable {consumable.name} was updated successfully"}

@consumable_router.get("/{id}/check")
@consumable_decorator_exception
def check_conumable(id: int,
                    car_id: str,
                    current_user = Depends(get_current_user)
) -> dict:
    message = consumable_service.check(id)
    return {"msg": message}

@consumable_router.delete("/{id}")
@consumable_decorator_exception
def delete_conumable(id: int,
                    current_user = Depends(get_current_user)
) -> dict:
    consumable_service.delete(id)
    return {"msg": f"Consumable was deleted successfully"}
