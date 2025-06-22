from fastapi import APIRouter, Depends

from core.cars.services import car_service
from api.rest.users.dependencies import get_current_user
from .schemas import CarSchema
from .decorators import car_exception

car_router = APIRouter(prefix="/cars", tags=["Cars"])


@car_router.post("/add")
@car_exception
def add_car(car: CarSchema, user = Depends(get_current_user)) -> dict:
    car_service.add(car, user)
    return {"msg": "Car was added successfully"}

@car_router.get("/{id}")
@car_exception
def get_car(id: int, user = Depends(get_current_user)) -> CarSchema:
    return car_service.get(id)

@car_router.get("/")
@car_exception
def get_all_cars(user = Depends(get_current_user)) -> list[CarSchema]:
    return car_service.get_all(user.id)


@car_router.put("/{id}")
@car_exception
def update_car(id: int, car: CarSchema, user = Depends(get_current_user)) -> dict:
    car_service.update(id, car, user)
    return {"msg": "Car was updated successfully"}

@car_router.delete("/{id}")
@car_exception
def delete_car_by_name(id: int, user = Depends(get_current_user)) -> dict:
    car_service.delete(id)
    return {"msg": "Car was deleted successfully"}
    