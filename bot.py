import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from utils.scheduler import start_scheduler
from config import BOT_TOKEN
from handlers import registration, weather, help
from database.db import init_db
from middlewares.db_middleware import DbSessionMiddleware

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Помощь по командам"),
        BotCommand(command="weather", description="Текущая погода"),
        BotCommand(command="set_times", description="Настроить время уведомлений"),
        BotCommand(command="change_city", description="Изменить город"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DbSessionMiddleware())

    await init_db()
    await set_bot_commands(bot)

    dp.include_router(help.router)
    dp.include_router(registration.router)
    dp.include_router(weather.router)

    start_scheduler(bot)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())