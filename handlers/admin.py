from config import Bot, F, Router, FSInputFile, types, FSMContext, State, bot, CallbackData, FSInputFile
from markups.adminmarkup import *
import filters.filtersbot as filtersbot
from sql_function import databasework
import filters.filtersbot as filtersbot
    
router = Router()

router.message.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру
router.callback_query.filter(filtersbot.AdminCheck()) # привязываем фильтр к роутеру







@router.message(F.text == '/admin', F.chat.type == 'private')
async def start(message: types.Message, state: FSMContext):
    #photo = FSInputFile('kwork8/photo/start_message.jpg')
    await state.clear()
    markup = admin_markup()
    await message.answer(f'💎 Вы попали в админ-панель', reply_markup=markup)
    
    
    
    
admin = router
