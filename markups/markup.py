from config import types, InlineKeyboardBuilder
import filters.filtersbot as filtersbot
from sql_function import databasework


def start_markup(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='✔️ Добавить токен', callback_data='add_token') # 
        .adjust(2, repeat=True)
        .as_markup()
    )
    
    return markup

def menu(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='✔️ На главную', callback_data='main_menu') # 
        .adjust(2, repeat=True)
        .as_markup()
    )
    
    return markup

def menu2(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='✔️ На главную', callback_data='main_menu') # 
        .button(text='✔️ Отменить', callback_data='cancel') # 
        .adjust(1, repeat=True)
        .as_markup()
    )
    
    return markup

def networks_markup(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='Solana', callback_data='solscan') # 
        .button(text='Ton', callback_data='tonscan') # 
        .button(text='Ethereum', callback_data='etherscan') # 
        .button(text='Base', callback_data='basescan') # 
        .button(text='Tron', callback_data='tronscan') # 
        .button(text='✔️ На главную', callback_data='main_menu') # 
        .adjust(2, repeat=True)
        .as_markup()
    )
    
    return markup


def token_markup(): # старт кнопки

    markup = (
        InlineKeyboardBuilder()
        .button(text='Опубликовать пост', callback_data='pub_post') # 
        .button(text='Изменить текст', callback_data='edit_text') # 
        .button(text='Изменить фото', callback_data='edit_photo') # 
        .button(text='✔️ На главную', callback_data='main_menu') # 
        .adjust(1, 2, repeat=True)
        .as_markup()
    )
    
    return markup






