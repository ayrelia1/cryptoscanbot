from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict

class CallbackMiddleware(BaseMiddleware): # ---- > мидлвар кнопок
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        bot: Bot = data["bot"]

        
        
        await bot.answer_callback_query(event.from_user.id)

        

        return await handler(event, data)
    
