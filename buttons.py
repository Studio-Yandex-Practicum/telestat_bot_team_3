from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bot_1_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Добавить администратора'),
        KeyboardButton(text='Удалить администратора'),
    ],
    [
        KeyboardButton(text='Выбрать телеграм канал'),
        KeyboardButton(text='Установить период сбора данных'),
    ],
    [
        KeyboardButton(text='Начать сбор аналитики')
    ]


], resize_keyboard=True,
   placeholder='add_admin @username1, @username2, @... , del_admin @username, '
               'choise_channel, set_period, generate_report'
)


bot_2_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Добавить администратора'),
        KeyboardButton(text='Удалить администратора'),
    ],
    [
        KeyboardButton(text='Автоматическое формирование отчёта'),
        KeyboardButton(text='Формирование отчёта'),
    ],
    [
        KeyboardButton(text='Формирование графика')
    ]
], resize_keyboard=True)
