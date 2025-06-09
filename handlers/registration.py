from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters.command import CommandObject
from sqlalchemy.future import select
from database.models import User
from aiogram.fsm.context import FSMContext
from states import RegistrationStates

router = Router()

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await message.answer(
        "Привет! Я бот для отслеживания погоды.\n"
        "Для начала работы отправь мне название своего города."
    )
    await state.set_state(RegistrationStates.waiting_for_city)

@router.message(Command("change_city"))
async def change_city_cmd(message: Message, state: FSMContext):
    await message.answer("Введите новый город:")
    await state.set_state(RegistrationStates.waiting_for_city)

@router.message(RegistrationStates.waiting_for_city, F.text)
async def process_city(message: Message, session, state: FSMContext):
    city = message.text.strip()
    if len(city) < 2 or len(city) > 50:
        await message.answer("Название города должно быть от 2 до 50 символов.")
        return

    stmt = select(User).where(User.telegram_id == message.from_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        user.city = city
    else:
        user = User(
            telegram_id=message.from_user.id,
            city=city,
            notify_times="09:00,14:00,22:00"
        )
        session.add(user)

    await session.commit()
    await state.clear()
    await message.answer(
        f"Город {city} сохранён!\n"
        f"Теперь вы можете получать прогноз погоды с помощью команды /weather\n"
        f"И настроить уведомления с помощью /set_times"
    )

@router.message(Command("set_times"))
async def set_notify_times(message: Message, command: CommandObject, session):
    times = command.args
    if not times:
        await message.answer(
            "Укажите времена уведомлений через запятую, например:\n"
            "/set_times 09:00,14:00,22:00\n"
            "Можно указать до 5 временных точек."
        )
        return

    time_list = [t.strip() for t in times.split(",") if t.strip()]
    if len(time_list) > 5:
        await message.answer("Можно указать не более 5 временных точек.")
        return

    for time_str in time_list:
        try:
            hours, minutes = map(int, time_str.split(":"))
            if not (0 <= hours < 24 and 0 <= minutes < 60):
                raise ValueError
        except ValueError:
            await message.answer(f"Некорректный формат времени: {time_str}")
            return

    stmt = select(User).where(User.telegram_id == message.from_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        user.notify_times = ",".join(time_list)
        await session.commit()
        await message.answer(f"Времена уведомлений обновлены: {', '.join(time_list)}")
    else:
        await message.answer("Сначала укажите город с помощью /start.")