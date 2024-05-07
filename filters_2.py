from pyrogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)


# Здесь попытался адаптировать пример из библиотеки Pyrogram через Inline
# кнопки: https://docs.pyrogram.org/start/examples/bot_keyboards
bot_1_2_filters_keyboard = InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton(
                            "1 час",
                            callback_1_hour="1_hour"
                        ),
                        InlineKeyboardButton(
                            "5 часов",
                            callback_5_hour="5_hour"
                        ),
                    ],
                    [  # Second row
                        InlineKeyboardButton(
                            "10 час",
                            callback_10_hour="10_hour"
                        ),
                        InlineKeyboardButton(
                            "15 часов",
                            callback_15_hour="15_hour"
                        ),
                    ],
                    [  # Third row
                        InlineKeyboardButton(
                            "24 час",
                            callback_24_hour="24_hour"
                        ),
                        InlineKeyboardButton(
                            "Произвольное время в часах",
                            switch_inline_query_current_chat="pyrogram"
                        ),
                    ]
                ]
            )
