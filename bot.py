from typing import Union

from aiogram import Bot,Dispatcher,types
from handlers.image_prepare import router as img_prepare_router
import asyncio
from config import config_sets
import logging
from aiogram.handlers import ErrorHandler
from aiogram import BaseMiddleware

bot = Bot(token=config_sets.token.get_secret_value())
dp = Dispatcher()

logging.basicConfig(level = logging.INFO)

async def main():
    dp.include_routers(img_prepare_router)
    await dp.start_polling(bot)
asyncio.run(main())

#загрузить изображение предобработать его( сделать чернобелым и )
# и сохранить в новую папку обработанных изображений


