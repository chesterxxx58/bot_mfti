from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any
from aiogram.types import TelegramObject
from database.db import SessionLocal

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with SessionLocal() as session:
            data["session"] = session
            return await handler(event, data)