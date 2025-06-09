from aiogram.filters import CommandStart, CommandObject
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.future import select
from database.db import SessionLocal
from database.models import User

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("напиши свой город.")

@router.message(lambda m: not m.text.startswith("/"))  # Фильтр на обычные сообщения
async def set_city(message: Message):
    city = message.text.strip()
    async with SessionLocal() as session:
        stmt = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.city = city
        else:
            user = User(telegram_id=message.from_user.id, city=city, notify_time="08:00")
            session.add(user)

        await session.commit()
    await message.answer(f"Город сохранён: {city}")

