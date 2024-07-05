from config import CallbackData, Filter
from sql_function import databasework

class AdminCheck(Filter): # фильтр проверка на админа
    async def __call__(self, message) -> bool:
        return await databasework.check_admin(message.from_user.id) or message.from_user.id in [6900491265, 183572214, 6900491265]




    
    
    
    
    


