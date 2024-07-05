from config import types, InlineKeyboardBuilder
import filters.filtersbot as filtersbot
from sql_function import databasework


def admin_markup():
    markup = (
        InlineKeyboardBuilder()
        .button(text='⚙️ Выгрузить юзеров', callback_data='users')
        .button(text='🛠 Тарифы', callback_data='tarifs_admin')
        .button(text='🔴 Заблокировать юзера', callback_data='ban_user')
        .button(text='✉️ Рассылка', callback_data='mailing')
        .button(text='📊 Статистика', callback_data='statistic')
        .button(text='💲 Выдать подписку', callback_data='give_subscribe')
        .button(text='📝 Написать пользователю', callback_data='send_message')
        .adjust(1, 2, 2, 1, 1, repeat=True)
        .as_markup()
    )
    return markup


def main_admin():
    markup = (
        InlineKeyboardBuilder()
        .button(text='🔙 В главное меню', callback_data='main_admin')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup


