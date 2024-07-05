from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from sql_function import databasework
from db.models import UserData

class BannedMiddleware(BaseMiddleware): # ---- > мидлвар чек на бан
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        
        data["bot_user"]: UserData = await databasework.check_user_o(event.from_user.id)
        
        
        #check_ban = await databasework.check_ban(event.from_user.id) # проверяем на бан
        if data["bot_user"].ban == 'yes': # проверка бана
            bot: Bot = data["bot"]
            return await bot.send_message(event.from_user.id, (f'Banned!'))

        return await handler(event, data)