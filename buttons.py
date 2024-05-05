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
], resize_keyboard=True)


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

add_users_key = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    'Введите пользователей для добавления в базу',
                    callback_data='callback_data')]
            ])
