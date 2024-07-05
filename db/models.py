from dataclasses import dataclass
from db.db import engine, async_session

from sqlalchemy import BigInteger, text
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, String, CheckConstraint, UniqueConstraint, Float, DateTime





class Base(AsyncAttrs, DeclarativeBase):
    pass

# Модель для таблицы `users`
class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(String(100), unique=True, index=True)
    username = mapped_column(String(100), default=None)  # На уровне Python
    
    status = mapped_column(
        String(25),
        CheckConstraint("status IN ('user', 'admin')"),  # Позиционный аргумент перед именованными
        default='user',  # На уровне Python
        server_default='user',  # На уровне базы данных
    )
    
    subscribe = mapped_column(
        String(25),
        CheckConstraint("subscribe IN ('on', 'off')"),
        default='off',  # На уровне Python
        server_default='off',  # На уровне базы данных
    )
    
    reg_date = mapped_column(
        String(50),
        server_default=text("CURRENT_TIMESTAMP"),  # На уровне базы данных
    )
    
    ban = mapped_column(
        String(25),
        CheckConstraint("ban IN ('yes', 'no')"),
        default='no',  # На уровне Python__annotat__annotations__())ons__())
        server_default='no',  # На уровне базы данных
    )



class Tokens(Base):
    __tablename__ = 'tokens'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    address = mapped_column(String(100), index=True)
    price = mapped_column(Float)
    name = mapped_column(String(100), index=True)
    symbol = mapped_column(String(100), index=True)
    history = mapped_column(
        Integer, 
        default=1,
        server_default=1,
    )
    datetime = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    channel_id = mapped_column(Integer())
    message_id = mapped_column(Integer())




async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from dataclasses import dataclass

@dataclass
class UserData:
    id: int
    user_id: str
    username: str
    status: str
    subscribe: str
    reg_date: str
    ban: str