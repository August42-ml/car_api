from fastapi import APIRouter, Depends

from core.cars.services import car_service
from api.rest.users.dependencies import get_current_user
from .schemas import CarSchema
from .decorators import car_exception

car_router = APIRouter(prefix="/cars", tags=["Cars"])


@car_router.post("/add")
@car_exception
def add_car(car: CarSchema, user = Depends(get_current_user)) -> dict:
    car_service.add(car)
    return {"msg": "Car was added successfully"}

@car_router.get("/{name}")
@car_exception
def get_car(name: str, user = Depends(get_current_user)) -> CarSchema:
    return car_service.get(name)

@car_router.put("/{name}")
@car_exception
def update_car(name: str, car: CarSchema, user = Depends(get_current_user)) -> dict:
    car_service.update(name, car)
    return {"msg": "Car was updated successfully"}

@car_router.delete("/{name}")
@car_exception
def delete_car(name: str, user = Depends(get_current_user)) -> dict:
    car_service.delete(name)
    return {"msg": "Car was deleted successfully"}
    