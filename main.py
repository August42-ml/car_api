from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from asyncio import create_task, CancelledError

from database.connection import connect
from routes import car, notification
from config import settings 
from bot.bot import bot, dp
from bot.handler import main_tg_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #коннект с бд
    connect()
    
    #запуск бота
    dp.include_router(main_tg_router)
    bot_task = create_task(dp.start_polling(bot))

    yield
    
    bot_task.cancel()
    try:
        await bot_task
    except CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(car.car_router, prefix="/car")
app.include_router(notification.notification_router, prefix="/notification")

@app.get('/')
async def welcome() -> dict:
    return {"msg": "Welcome"} 

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)