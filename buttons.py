from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assistants.assistants import DotNotationDict

bot_keyboard = [
    {
        'key_name': 'Добавить администратора'
    },
    {
        'key_name': 'Удалить администратора'
    },
    {
        'key_name': 'Выбрать телеграм канал'
    },
    {
        'key_name': 'Установить период сбора данных'
    },
    {
        'key_name': 'Начать сбор аналитики'
    },
    {
        'key_name': 'Автоматическое формирование отчёта'
    },
    {
        'key_name': 'Формирование отчёта'
    },
    {
        'key_name': 'Формирование графика'
    }
]

bot_keys = []
for dict_out in bot_keyboard:
    bot_keys.append(DotNotationDict(dict_out))
