from fastapi import APIRouter, Depends

from core.consumable.services import consumable_service
from api.rest.users.dependencies import get_current_user
from .schemas import ConsumableSchema
from .decorators import consumable_decorator_exception

consumable_router = APIRouter(prefix="/consumables", tags=["Consumables"])

@consumable_router.get("/{name}")
@consumable_decorator_exception
def get_consumable(name: str, current_user = Depends(get_current_user)) -> ConsumableSchema:
    return consumable_service.get(name)

@consumable_router.post("/add")
@consumable_decorator_exception
def add_consumable(consumable: ConsumableSchema, current_user = Depends(get_current_user)) -> dict:
    consumable_service.add(consumable)
    return {"msg": f"Consumable {consumable.name} was added successfully"}

@consumable_router.put("/{name}")
@consumable_decorator_exception
def update_consumable(name: str, consumable: ConsumableSchema, current_user = Depends(get_current_user)) -> dict:
    consumable_service.update(name, consumable)
    return {"msg": f"Consumable {consumable.name} was updated successfully"}

@consumable_router.get("/{name}/check")
@consumable_decorator_exception
def check_conumable(name: str, car_name: str, current_user = Depends(get_current_user)) -> dict:
    message = consumable_service.check(name, car_name)
    return {"msg": message}

@consumable_router.delete("/{name}")
@consumable_decorator_exception
def delete_conumable(name: str, current_user = Depends(get_current_user)) -> dict:
    consumable_service.delete(name)
    return {"msg": f"Consumable {name} was deleted successfully"}
