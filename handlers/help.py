from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_cmd(message: Message):
    help_text = (
        "📌 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/weather - Текущая погода в вашем городе\n"
        "/set_times - Настроить время уведомлений\n"
        "/change_city - Изменить город\n\n"
        "⏰ <b>Формат времени уведомлений:</b>\n"
        "/set_times 09:00,14:00,22:00\n\n"
        "🌍 <b>Поддерживаются города по всему миру</b>"
    )
    await message.answer(help_text)