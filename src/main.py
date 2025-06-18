from fastapi import FastAPI, APIRouter

from api.rest.cars.views import car_router
from api.rest.users.views import user_router
from api.rest.consumable.views import consumable_router

app = FastAPI()

main_v1_router = APIRouter(prefix="/v1/api")
main_v1_router.include_router(car_router)
main_v1_router.include_router(user_router)
main_v1_router.include_router(consumable_router)
app.include_router(main_v1_router)
