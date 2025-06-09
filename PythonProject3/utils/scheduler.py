from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select
from database.db import SessionLocal
from database.models import User
from weather.api import get_weather
from aiogram import Bot

scheduler = AsyncIOScheduler()

async def send_daily_weather(bot: Bot):
    async with SessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()

        for user in users:
            weather = get_weather(user.city)
            try:
                await bot.send_message(chat_id=user.telegram_id, text=f"Ежедневная погода:\n{weather}")
            except Exception as e:
                print(f"ошибка {user.telegram_id}: {e}")

def start_scheduler(bot: Bot):
    scheduler.add_job(send_daily_weather, "cron", hour=9, minute=0, args=[bot])  # отправка в 9 утра каждый день
    scheduler.start()
