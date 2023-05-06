from aiogram import Bot, Dispatcher
import dotenv
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage

dotenv.load_dotenv()

storage = MemoryStorage()

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
