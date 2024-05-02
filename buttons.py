from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton


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
