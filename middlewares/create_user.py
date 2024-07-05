from aiogram.types import Message, CallbackQuery
from config import settings
from aiogram import Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from sql_function import databasework


class CreateUserMiddleware(BaseMiddleware): # ---- > мидлвар создание юзера
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        
        
        
        check_user = await databasework.check_user(event.from_user.id) # ---> достаем юзера
        if check_user == None: # если юзера нет - 
            await databasework.create_user(event.from_user.id, event.from_user.username) # - создаем 
            
            
        elif check_user[2] != event.from_user.username: # обновляем юзернейм если изменился
            await databasework.update_username_user(event.from_user.username, event.from_user.id)
        
        
        
        return await handler(event, data)
        
