from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.future import select
from database.db import SessionLocal
from database.models import User
from weather.api import get_weather

router = Router()  # Создаем роутер

@router.message(Command("weather"))
async def get_weather_cmd(message: Message):
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            weather_info = get_weather(user.city)
            await message.answer(weather_info)
        else:
            await message.answer("Сперва скажи свой город.")
