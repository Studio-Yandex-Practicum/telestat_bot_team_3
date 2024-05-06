from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton


bot_1_2_filters_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='1 час'),
        KeyboardButton(text='5 часов'),
    ],
    [
        KeyboardButton(text='10 часов'),
        KeyboardButton(text='15 часов'),
    ],
    [
        KeyboardButton(text='24 часа'),
        KeyboardButton(text=f'Произвольное время: {int}'),
    ]
], resize_keyboard=True)
