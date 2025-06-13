from fastapi import FastAPI, APIRouter
import uvicorn

from cars.views import car_router
from users.views import user_router
from config import settings 

app = FastAPI()

main_v1_router = APIRouter(prefix="/v1/api")
main_v1_router.include_router(car_router)
main_v1_router.include_router(user_router)

app.include_router(main_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)