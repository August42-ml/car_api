from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from .bot import bot
from config import settings

main_tg_router = Router()

#сообщение при старте
@main_tg_router.message(Command('start'))
async def start_message(start_message: Message) -> None:
    await start_message.answer(text="Bot was started")


async def send_warning(warning: str) -> None:
    await bot.send_message(chat_id=settings.CHAT_ID, text=warning)