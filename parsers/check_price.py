import aiohttp
from config import settings, texts, current_directory
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
            result_x = await track_token_price(token[0], token[3], token[1], token[6])
            if result_x:
                channel_id = token[8]
                message_id = token[9]
                network = token[2]
                mcap = result_x['mcap']
                symbol = token[5]
                x = result_x['new_multiplier']
                
                
                text = texts[f"x_template_{network}"].format(network=network, mcap=mcap, x=x, symbol=symbol)
                
                if result_x['percent_change'] > 99 and result_x['percent_change'] < 3001:
                    
                    photo_path = current_directory + f"/assets/{str(result_x['percent_change'])}.jpg"
                    
                    async with Client("my_account", api_id=settings.API_ID, api_hash=settings.API_HASH) as app:
                        await app.send_photo(caption=text, photo=photo_path, chat_id=channel_id, reply_to_message_id=message_id)
                
                else:
                    async with Client("my_account", api_id=settings.API_ID, api_hash=settings.API_HASH) as app:
                        await app.send_message(text=text, chat_id=channel_id, reply_to_message_id=message_id, disable_web_page_preview=True)
            
    except Exception as ex:
        logging.error(traceback.format_exc())
        
        
    
    
def format_number(num, precision=12):
    return format(num, f'.{precision}f')

    
    
    
async def get_token_price(address):
    link = f'https://api.dexscreener.com/latest/dex/tokens/{address}'
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            resp = await response.text()
            
    response = json.loads(resp)
    return (response['pairs'][0]['priceUsd'], response['pairs'][0]['fdv'], response['pairs'][0]['baseToken']['symbol'])
    
    
    

async def track_token_price(id_token, initial_price, address, max_notified_multiplier):


    try:
        current_price, mcap, symbol = await get_token_price(address)
        current_price = float(format_number(float(current_price)))
        initial_price = float(format_number(float(initial_price)))
        multiplier = current_price / initial_price
        # Проверка новых кратностей
        new_multiplier = int(multiplier)
        new_multiplier_float = round(multiplier, 1)
        percent_change = (new_multiplier - 1) * 100
        
        crat = [(1.4, 1.6), (1.6, 1.8), [1.8, 2]]
        
        for i in crat:
            if new_multiplier_float >= i[0] and new_multiplier_float <= i[1] and new_multiplier_float > max_notified_multiplier:
                await databasework.update_max_notified_multiplier_token(i[1], id_token)
            
                data = {
                    "new_multiplier": round(new_multiplier_float, 1),
                    "mcap": mcap,
                    "current_price": current_price,
                    "symbol": symbol,
                    "percent_change": percent_change
                }
                
                return data
        
        
        if new_multiplier > 100:
            return None
        if new_multiplier > max_notified_multiplier:
            print(f"Token price has reached {new_multiplier}x: {current_price}")
            await databasework.update_max_notified_multiplier_token(new_multiplier, id_token)
            
            data = {
                "new_multiplier": new_multiplier,
                "mcap": mcap,
                "current_price": current_price,
                "symbol": symbol,
                "percent_change": percent_change
            }
            
            return data
        
        
        
        return None

    except Exception as e:
        logging.error(f"An error occurred: {e}")
