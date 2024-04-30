import asyncio

from pyrogram import Client, filters
from pyrogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            messages_and_media)

# from core.base import Base
# from core.db import engine
from settings import Config, configure_logging
from permissions.permissions import check_authorization

# async def init_models():
#     """Для проверки создаём таблицу в ручную."""

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_models())


logger = configure_logging()

app = Client(
    'my_account',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN)


keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='начать сбор аналитики'
        )
    ]

], one_time_keyboard=True, resize_keyboard=True)


@app.on_message(filters.command('start'))
async def command_start(client: Client, message: messages_and_media.message.Message):
    logger.info('Проверка на авторизацию')

    if not await check_authorization(message.chat.username):
        await client.send_message(message.chat.id, 'Управлять ботом могут только Администраторы.')
    else:
        await client.send_message(message.chat.id, 'Вы прошли авторизацию!', reply_markup=keyboard)
        logger.debug('Вы прошли авторизацию!')

        @app.on_message(filters.text == 'начать сбор аналитики')
        async def collect_analitycs(client: Client, message: messages_and_media.message.Message):
            logger.info('Бот начал работу')
            await client.send_message(message.chat.id, '...Здесь идет активный сбор данных пользователей...')
            logger.info('...Здесь идет активный сбор данных пользователей...')


asyncio.run(app.run())
