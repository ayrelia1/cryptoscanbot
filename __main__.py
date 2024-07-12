from config import dp, logging, bot, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from middlewares import setup
from handlers import routers
import asyncio
from db.models import create_tables
from db.db import engine
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parsers.check_price import check_price_token

import sys


#

@dp.startup()
async def start_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='🔄 Главное меню'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(check_price_token, 'interval', seconds=10)
    scheduler.start()
    
    task1 = asyncio.create_task(create_tables()) # создаем базу юзеров если нет

    
@dp.shutdown()
async def dispose(bot: Bot):
    
    engine.dispose()

            
                

async def main() -> None:     # функция запуска бота
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s" 
                        ) # логирование
    


    
    for router in routers:
        dp.include_router(router) # импорт роутеров
        
        
    setup(dp)  # мидлвари    
    try:
        await dp.start_polling(bot) # запуск поллинга
    except Exception as ex:
        print(ex)

        
    
if __name__ == "__main__":
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # устанавливаем политику для лупа если wind
            
    
    asyncio.run(main()) 
