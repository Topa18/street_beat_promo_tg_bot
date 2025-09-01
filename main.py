# import logging
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hlink, hbold

import bot.keyboards as kbs
from bot.handlers import router
from bot.config import TOKEN
from scrapper.discount_parser import get_pages_qty, get_data


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

try:
    # logging.basicConfig(level=logging.INFO)
    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    print("Bot execution stopped.")
except Exception as e:
    print(e)
