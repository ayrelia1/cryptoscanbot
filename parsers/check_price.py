import aiohttp
from config import settings
from sql_function import databasework
import json
import aiohttp
import asyncio
import logging
import traceback
from pyrogram import Client

async def check_price_token():
    try:
        tokens = await databasework.get_all_tokens()
        for token in tokens:
            result_x = await track_token_price(token[0], token[2], tokens[1], tokens[5])
            channel_id = token[7]
            message_id = token[8]
            
            async with Client("my_account", api_id=settings.API_ID, api_hash=settings.API_HASH) as app:
                await app.send_message(text='', chat_id=channel_id, reply_to_message_id=message_id)
            
    except Exception as ex:
        logging.error(traceback.format_exc())
        
        
    
    
    
    
    
async def get_token_price(address):
    link = f'https://api.dexscreener.com/latest/dex/tokens/{address}'
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            resp = await response.text()
            
    response = json.loads(resp)
    return response['pairs'][0]['priceUsd']
    
    
    

async def track_token_price(id_token, initial_price, address, max_notified_multiplier):


    try:
        current_price = await get_token_price(address)
        multiplier = current_price / initial_price

        # Проверка новых кратностей
        new_multiplier = int(multiplier)
        if new_multiplier > 100:
            return # до сотни
        if new_multiplier > max_notified_multiplier:
            print(f"Token price has reached {new_multiplier}x: {current_price}")
            await databasework.update_max_notified_multiplier_token(new_multiplier, id_token)
            return new_multiplier

    except Exception as e:
        logging.error(f"An error occurred: {e}")
