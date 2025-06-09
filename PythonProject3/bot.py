import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from utils.scheduler import start_scheduler
from config import BOT_TOKEN
from handlers import registration, weather
from database.db import init_db

async def main():
    # экземпляр бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # диспетчер
    dp = Dispatcher(storage=MemoryStorage())

    # инииализация баззы данных
    await init_db()

    # команды в бота тг
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="weather", description="Узнать погоду в вашем городе"),
    ])

    # регитсрация и погода
    dp.include_router(registration.router)
    dp.include_router(weather.router)

    # планировщик
    start_scheduler(bot)

    # полинг
    await dp.start_polling(bot)

# меин
if __name__ == "__main__":
    asyncio.run(main())
