from pyrogram import Client, filters, types, enums
from pyrogram.handlers import message_handler
from pyrogram.types import Message, ChatMember
import datetime
import random
import string
import json
import asyncio

api_id = 25194304
api_hash = '87b575cea6136435084cb763b42e359d'

client = Client('my_account', api_hash=api_hash, api_id=api_id)

       
        
@client.on_message()
async def asd(client, message):
    print(message.chat.id)   
    await client.send_photo(chat_id=-1002163207563, caption='123', photo="AgACAgQAAxkBAAPRZoVkhOMr6gzxhKwnEEMSaa75Y1QAAiDEMRtjozBQHgqLziIpgPkBAAMCAAN4AAM1BA")

    # Запускаем клиент
    


client.run()
    
    
    
async def echo(client: Client, message: Message):
    entities = message.entities or []

    # Пример HTML-шаблона для замены эмодзи
    emoji_template = '<emoji id={custom_emoji_id}>{emoji}</emoji>'

    # Исходный текст
    original_text = message.text

    # Список для сбора фрагментов текста с заменёнными эмодзи
    replaced_parts = []

    # Переменная для отслеживания текущей позиции в тексте
    current_position = 0

    # Проход по каждой сущности
    for entity in entities:
        if entity.type == enums.MessageEntityType.CUSTOM_EMOJI:
            start_offset = entity.offset
            end_offset = start_offset + entity.length

            # Добавляем часть текста между текущей позицией и началом сущности
            replaced_parts.append(original_text[current_position:start_offset])

            # Заменяем эмодзи только для сущностей типа CUSTOM_EMOJI
            custom_emoji_id = entity.custom_emoji_id
            emoji = f'🌟'  # Здесь нужно получать эмодзи по его идентификатору
            replaced_parts.append(emoji_template.format(custom_emoji_id=custom_emoji_id, emoji=emoji))

            # Обновляем текущую позицию до конца текущей сущности
            current_position = end_offset

    # Добавляем оставшуюся часть текста после последней сущности
    replaced_parts.append(original_text[current_position:])

    # Объединяем все части в одну строку
    replaced_text = ''.join(replaced_parts)

    # Отправляем изменённый текст обратно в чат
    await message.reply_text(replaced_text)