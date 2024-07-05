from config import *

from .check_ban import BannedMiddleware
from .create_user import CreateUserMiddleware
from .throttling import ThrottlingMiddleware

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
def setup(dp: Dispatcher):


    throttling_middleware = ThrottlingMiddleware()
    dp.message.outer_middleware.register(throttling_middleware)
    dp.callback_query.outer_middleware.register(throttling_middleware)

    create_user_middleware = CreateUserMiddleware()
    dp.message.outer_middleware.register(create_user_middleware)
    dp.callback_query.outer_middleware.register(create_user_middleware)

    banned_middleware = BannedMiddleware()
    dp.message.outer_middleware.register(banned_middleware)
    dp.callback_query.outer_middleware.register(banned_middleware)
    
    
    

    dp.callback_query.middleware(CallbackAnswerMiddleware())
    
    