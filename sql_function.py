from config import types
from db.db import async_session, engine
import sys, asyncio
from sqlalchemy import text
from sqlalchemy.future import select
from db.models import User, UserData
import datetime

class databasework:
    
    
    
    
    async def get_all_tokens():
        month_date = datetime.datetime.now() - datetime.timedelta(days=30)
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM tokens WHERE datetime > :month_date"
                result = await session.execute(text(sql), {"month_date": month_date})
            return result.all()  # Возвращает все строки
    
    async def update_max_notified_multiplier_token(max_notified_multiplier: int, id: int):
        async with async_session() as session:
            async with session.begin():
                sql = "UPDATE tokens SET history = :history WHERE id = :id"
                await session.execute(text(sql), {"history": max_notified_multiplier, "id": id})
            await session.commit()
    
    
    async def ins_token(address: str, network: str, price: float, name: str, symbol: str, channel_id: int, message_id: int):
        async with async_session() as session:
            async with session.begin():
                sql = """
                INSERT INTO tokens (address, network, price, name, symbol, channel_id, message_id)
                VALUES (:address, :price, :network, :name, :symbol, :channel_id, :message_id)
                """
                await session.execute(text(sql), {"address": str(address), "network": str(network), "price": float(price), "name": str(name), "symbol": str(symbol), "channel_id": channel_id, "message_id": message_id})
            await session.commit()  # Подтверждение транзакции
    
    
    async def create_user(user_id: str, username: str):
        async with async_session() as session:
            async with session.begin():
                sql = """
                INSERT INTO users (user_id, username)
                VALUES (:user_id, :username)
                """
                await session.execute(text(sql), {"user_id": str(user_id), "username": username})
            await session.commit()  # Подтверждение транзакции
    
    async def update_username_user(username: str, user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "UPDATE users SET username = :username WHERE user_id = :user_id"
                await session.execute(text(sql), {"username": username, "user_id": str(user_id)})
            await session.commit()
    
        
    async def check_user(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                
                return result.one_or_none() # Возвращает один результат или None
            
            
    async def check_user_o(user_id: str):
        async with async_session() as session:
            async with session.begin():
                stmt = select(User).where(User.user_id == str(user_id))  # Используем ORM-запрос
                result = await session.execute(stmt)  # Выполнение запроса
                user = result.scalar_one_or_none()  # Получение первого ORM-объекта
                
                user_data = UserData(
                    id=user.id,
                    user_id=user.user_id,
                    username=user.username,
                    status=user.status,
                    subscribe=user.subscribe,
                    reg_date=user.reg_date,
                    ban=user.ban,
                )
                
                
                return user_data  # Возвращает экземпляр `dataclass`
                
  
                
    async def check_ban(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                ban_status = result.one_or_none()  # Получение значения
                return ban_status and ban_status[7] == 'yes'
        
        

    async def check_admin(user_id: str):
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users WHERE user_id = :user_id"
                result = await session.execute(text(sql), {"user_id": str(user_id)})
                status = result.one_or_none()  # Получение статуса пользователя
                if status:
                    return status[4] == 'admin'
                return 
    
    
    
    async def get_all_users():
        async with async_session() as session:
            async with session.begin():
                sql = "SELECT * FROM users"
                result = await session.execute(text(sql))  # Выполнение запроса
                return result.all()  # Возвращает все строки
    
    
