from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.future import select
from database.models import User
from weather.api import get_weather
from datetime import datetime

router = Router()

@router.message(Command("weather"))
async def get_weather_cmd(message: Message, session):
    stmt = select(User).where(User.telegram_id == message.from_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not user.city:
        await message.answer(
            "Сначала укажите город с помощью команды /start.\n"
            "Или измените город с помощью /change_city"
        )
        return

    try:
        weather_info = get_weather(user.city)
        await message.answer(weather_info)
    except Exception as e:
        await message.answer("Произошла ошибка при получении погоды. Попробуйте позже.")
        print(f"Weather error: {e}")