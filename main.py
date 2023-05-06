from aiogram import executor
from config import dp
from bot import register_handlers_client


if __name__ == '__main__':
    register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)
