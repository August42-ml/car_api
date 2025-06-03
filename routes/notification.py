from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


from bot.handler import send_warning

notification_router = APIRouter(tags=['notification'])

@notification_router.post('/')
async def send_warning_by_bot(warning: str) -> dict:
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            func=send_warning,
            trigger="date",
            run_date=datetime.now(),
            kwargs={
                "warning": warning
            }
        )
        scheduler.start()
        return {"msg": "Message was successfully sended"}
    except TypeError:
        return {"msg": "Something goes wrong with telegramm bot"}