from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)


# В данном фале сделал по аналогии с клавиатурой в файле buttons.py
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
        # Произвольное время выделил как кнопку в которой можно задавать число
        # int "f", исходя из теории, будет переводить в формат строки
        KeyboardButton(text=f'Произвольное время в часах: {int}'),
    ]
], resize_keyboard=True)
