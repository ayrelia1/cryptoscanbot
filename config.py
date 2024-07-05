from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from aiogram.types import FSInputFile
from aiogram.types import (
    KeyboardButton,
    Message,
    Update,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram import types
from aiogram.filters import Filter
import logging
import datetime
import json
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings



load_dotenv()

    
current_directory = os.path.abspath(os.path.dirname(__file__))

with open(f"{current_directory}/texts.json", encoding='UTF-8') as file:
    texts = json.load(file)

class Settings(BaseSettings): # создаем settings class
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    CHANNEL_ID: int = os.getenv("CHANNEL_ID")
    API_ID: int = os.getenv("api_id")
    API_HASH: str = os.getenv("api_hash")
    
        
settings = Settings()

     
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(settings.BOT_TOKEN, parse_mode="html")






