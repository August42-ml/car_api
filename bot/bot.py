from aiogram import Bot, Dispatcher


from config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher() # для взаимодейтсвия с ботом