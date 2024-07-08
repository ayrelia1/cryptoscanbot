import aiogram.exceptions
from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, FSInputFile, settings, texts, current_directory
from markups.markup import *
from aiogram.types.input_file import FSInputFile, InputFile
import filters.filtersbot as filtersbot
from sql_function import databasework
from states.states import RequestState
from datetime import timedelta
import datetime
import filters.filtersbot as filtersbot
from aiogram.types import Chat
from db.models import User
from parsers.solscan import Solscan
from parsers.etherscan import Etherscan
from parsers.basescan import Basescan
from parsers.tonscan import Tonscan
import re
import requests
from pyrogram import Client
import traceback
import logging
import json
import random
import os
import aiogram
from parsers.check_price import get_token_price

tonscan = Tonscan()
solscan = Solscan()
etherscan = Etherscan()
basescan = Basescan()

router = Router()



router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру


# @router.message()
# async def go_main(message: types.Message, state: FSMContext):
#     print(message.entities)
    
# меню
@router.callback_query(F.data == 'main_menu')
async def go_main(callback: types.CallbackQuery, state: FSMContext):
    
    
    await state.clear()
    markup = start_markup()
    await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    await bot.send_message(chat_id=callback.message.chat.id, text='⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)

# хендлер старта
@router.message(F.text == '/start', F.chat.type == 'private')
async def start(message: types.Message, state: FSMContext, bot_user: User):
    
    await state.clear()
    markup = start_markup()
    await message.answer(f'⭐️ Добро пожаловать в бота, используйте кнопки ниже', reply_markup=markup)
    
@router.callback_query(F.data == 'add_token')
async def add_token_handler(callback: types.CallbackQuery, state: FSMContext):
    markup = menu()
    await bot.edit_message_text(message_id=callback.message.message_id, chat_id=callback.message.chat.id, text='⭐️ Введите адрес токена', reply_markup=markup)
    await state.set_state(RequestState.one)
    
@router.message(RequestState.one, F.text)
async def add_token_handler(message: types.Message, state: FSMContext):
    data = await state.update_data(address=message.text)
    await state.set_state(RequestState.two)
    markup = networks_markup()
    await bot.send_message(chat_id=message.chat.id, text='⭐️ Выберите сеть', reply_markup=markup)


#говнокод on
@router.callback_query(RequestState.two, F.data.in_(['solscan', 'tonscan', 'etherscan', 'basescan']))
async def scan_token(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RequestState.three)
    data = await state.get_data()
    address = data['address']
    if callback.data == 'solscan':
        func = solscan.get_token_info
        text: str = texts['solscan']
        network = 'SOL'
        dexscreener = 'solana'
    if callback.data == 'tonscan':
        func = tonscan.get_token_info
        text: str = texts['tonscan']
        network = 'TON'
        dexscreener = 'ton'
    if callback.data == 'etherscan':
        func = etherscan.get_token_info
        text: str = texts['etherscan']
        network = 'ETH'
        dexscreener = 'ethereum'
    if callback.data == 'basescan':
        func = basescan.get_token_info
        text: str = texts['basescan']
        network = 'BASE'
        dexscreener = 'base'
        
    result = await func(address)
    if result.get('name', None) == None or result.get('symbol', None) == None:
        markup = menu()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Ошибка! Данные не были собраны!', reply_markup=markup)
        return
    
    telegram, website = '', ''
    if result['telegram']:
        telegram = f'\n\n{texts["telegram_emoji"]} {result["telegram"]}'
    if result['website'] and result['telegram']:
        website = f'\n{texts["website_emoji"]} {result["website"]}'
    elif result['website']:
        website = f'\n\n{texts["website_emoji"]} {result["website"]}'
        
    dexscreener_link = f"{texts['dexscreener_emoji']} https://dexscreener.com/{dexscreener}/{address}"
    
    if result['symbol'].startswith('$'):
        symbol = result['symbol']
    else:
        symbol = f"${result['symbol']}"
    
    text_message = text.format(network=network, symbol=symbol, address=address, telegram=telegram, website=website, dexscreener=dexscreener_link)
    print(text_message)
    
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    
    cleaned_text = await clean_text(text_message)
    
    markup = token_markup()
    if result['image']:
        try:
            await callback.message.answer_photo(caption=cleaned_text, photo=result['image'], parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
        except aiogram.exceptions.TelegramBadRequest:
            await callback.message.answer(cleaned_text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    else:
        await callback.message.answer(cleaned_text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    await state.update_data(network=network, text_message=text_message, cleaned_text=cleaned_text, image=result['image'], address=address, name=result['name'], symbol=symbol)
    
    
    
@router.callback_query(RequestState.three, F.data.in_(['pub_post']))
async def pub_post(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data['text_message']
    image = data['image']
    address = data['address']
    network = data['network']
    print(image)
    try:
        async with Client("my_account", api_id=settings.API_ID, api_hash=settings.API_HASH) as app:
            if image:
                image_path=data.get('image_path', None)
                if image_path:
                    msg = await app.send_photo(chat_id=-1002163207563, photo=image_path, caption=text)
                else:
                    msg = await app.send_photo(chat_id=-1002163207563, photo=image, caption=text)
            else:
                msg = await app.send_message(chat_id=-1002163207563, text=text, disable_web_page_preview=True)
        
        channel_id, message_id = msg.chat.id, msg.id
        
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
        await bot.send_message(chat_id=callback.message.chat.id, text='Отлично, пост отправлен!', reply_markup=menu(), disable_web_page_preview=True)
        price, mcap, symbol = await get_token_price(address)
        await databasework.ins_token(address, network, price, data['name'], data['symbol'], channel_id, message_id)
        
    except Exception as ex:
        await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
        await bot.send_message(chat_id=callback.message.chat.id, text='Ошибка, пост не был отправлен', reply_markup=menu(), disable_web_page_preview=True)
        logging.error(traceback.format_exc())
    
    
    

    
@router.callback_query(RequestState.three, F.data.in_(['edit_photo']))
async def edit_photo(callback: types.CallbackQuery, state: FSMContext):
    #await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    markup = menu2()
    await callback.message.answer('Отправьте фото', parse_mode='html', reply_markup=markup)
    await state.set_state(RequestState.four)
    
@router.message(RequestState.four, F.content_type.in_({'photo'}))
async def edit_photo(message: types.Message, state: FSMContext):
    random_number = random.randint(100000, 10000000000)
    try:
        os.remove(f"{current_directory}/assets/photo_{random_number}.jpg")
    except:
        pass
    
    photo = message.photo[-1]
    data = await state.get_data()
    text_message = data['text_message']
    cleaned_text = data['cleaned_text']
    
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path    
    
    media = f"{current_directory}/assets/photo_{random_number}.jpg"
    await bot.download_file(file_path, media)
    
    photo = FSInputFile(media)
    markup = token_markup()
    await state.update_data(image=photo, image_path=media)
    await message.answer_photo(caption=cleaned_text, photo=photo, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    await state.set_state(RequestState.three)
    
    
    

    
    
@router.callback_query(RequestState.three, F.data.in_(['edit_text']))
async def edit_text(callback: types.CallbackQuery, state: FSMContext):
    #await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    markup = menu2()
    await callback.message.answer('Отправьте новый текст', parse_mode='html', reply_markup=markup)
    await state.set_state(RequestState.four)
    
@router.message(RequestState.four, F.content_type.in_({'text'}))
async def edit_text(message: types.Message, state: FSMContext):
    
    data = await state.get_data()
    
    entities = message.entities or []

    # Пример HTML-шаблона для замены эмодзи
    emoji_template = '<emoji id="{custom_emoji_id}">{emoji}</emoji>'

    # Исходный текст
    original_text = message.text

    # Список для сбора фрагментов текста с заменёнными эмодзи
    replaced_parts = []

    # Переменная для отслеживания текущей позиции в тексте
    current_position = 0

    # Проход по каждой сущности
    for entity in entities:
        if entity.type == 'custom_emoji':
            start_offset = entity.offset
            end_offset = start_offset + entity.length

            # Добавляем часть текста между текущей позицией и началом сущности
            replaced_parts.append(original_text[current_position:start_offset])

            # Заменяем эмодзи только для сущностей типа CUSTOM_EMOJI
            custom_emoji_id = entity.custom_emoji_id
            emoji = original_text[start_offset:end_offset]  # Получаем эмодзи из текста
            replaced_parts.append(emoji_template.format(custom_emoji_id=custom_emoji_id, emoji=emoji))

            # Обновляем текущую позицию до конца текущей сущности
            current_position = end_offset

    # Добавляем оставшуюся часть текста после последней сущности
    replaced_parts.append(original_text[current_position:])

    # Объединяем все части в одну строку
    replaced_text = ''.join(replaced_parts)

    # Отправляем изменённый текст обратно в чат
    print(replaced_text)

    cleaned_text = await clean_text(replaced_text)

    await state.set_state(RequestState.three)
    
    markup = token_markup()
    if data['image']:
        
        await message.answer_photo(caption=cleaned_text, photo=data['image'], parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    else:
        await message.answer(cleaned_text, parse_mode='html', reply_markup=markup, disable_web_page_preview=True)
    await state.update_data(text_message=replaced_text, cleaned_text=cleaned_text)
    
    
    
@router.callback_query(RequestState.four, F.data == 'cancel')
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(message_id=callback.message.message_id, chat_id=callback.message.chat.id)
    await state.set_state(RequestState.three)
    
    
async def clean_text(text):
    cleaned_text = re.sub(r'<\/?emoji[^>]*>', '', text)
    return cleaned_text

user = router