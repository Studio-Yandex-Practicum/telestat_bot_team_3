from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from assistants.assistants import DotNotationDict

bot_1_keyboard = [
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
    }
]

# bot_1_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(text='Добавить администратора'),
#         KeyboardButton(text='Удалить администратора'),
#     ],
#     [
#         KeyboardButton(text='Выбрать телеграм канал'),
#         KeyboardButton(text='Установить период сбора данных'),
#     ],
#     [
#         KeyboardButton(text='Начать сбор аналитики')
#     ]


# ], resize_keyboard=True)


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

bot_1_key = []
for dict_out in bot_1_keyboard:
    bot_1_key.append(DotNotationDict(dict_out))
