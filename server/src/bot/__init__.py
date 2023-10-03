from aiogram import Bot

from src.bot import start
from src.config import settings


# Bot initialization
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")

bot_routers = [start.router]
