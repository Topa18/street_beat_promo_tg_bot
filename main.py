# import logging
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Bot, Dispatcher

from bot.handlers import router
from bot.handlers import include_notification
from bot.config import TOKEN


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await include_notification(dp, bot)

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
