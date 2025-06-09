from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select
from database.db import SessionLocal
from database.models import User
from weather.api import get_weather
from aiogram import Bot
from datetime import datetime

scheduler = AsyncIOScheduler()

async def send_weather_at_time(bot: Bot, time: str):
    async with SessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()

        for user in users:
            if not user.city or not user.notify_times:
                continue

            if time in user.notify_times.split(","):
                try:
                    weather = get_weather(user.city)
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"<b>Прогноз погоды на {time}</b>\n\n{weather}"
                    )
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")

def start_scheduler(bot: Bot):
    scheduler.add_job(
        send_weather_at_time,
        "cron",
        hour=9,
        minute=0,
        args=[bot, "09:00"],
        misfire_grace_time=60
    )
    scheduler.add_job(
        send_weather_at_time,
        "cron",
        hour=14,
        minute=0,
        args=[bot, "14:00"],
        misfire_grace_time=60
    )
    scheduler.add_job(
        send_weather_at_time,
        "cron",
        hour=22,
        minute=0,
        args=[bot, "22:00"],
        misfire_grace_time=60
    )

    scheduler.start()
