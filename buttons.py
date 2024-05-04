from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_bot_1_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text='Добавить администратора',
            callback_data='add_admin_bot_1'
        ),
        InlineKeyboardButton(
            text='Удалить администратора',
            callback_data='del_admin_bot_1'
        ),
    ],
    [
        InlineKeyboardButton(
            text='Выбрать телеграм канал',
            callback_data='choise_channel'
        ),
        InlineKeyboardButton(
            text='Установить период сбора данных',
            callback_data='set_period'
        ),
    ],
    [
        InlineKeyboardButton(
            text='Начать сбор аналитики',
            callback_data='run_collect_analitics'
        )
    ]
])


inline_bot_2_keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text='Добавить администратора',
            callback_data='add_admin_bot_2'
        ),
        InlineKeyboardButton(
            text='Удалить администратора',
            callback_data='del_admin_bot_2'
        ),
    ],
    [
        InlineKeyboardButton(
            text='Автоматическое формирование отчёта',
            callback_data='auto_report'
        ),
        InlineKeyboardButton(
            text='Формирование отчёта',
            callback_data='generate_report'
        ),
    ],
    [
        InlineKeyboardButton(
            text='Формирование графика',
            callback_data='scheduling'
        )
    ]
])
