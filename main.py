import asyncio

from pyrogram import Client, filters
from pyrogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            messages_and_media)

# from core.base import Base
# from core.db import engine
from settings import Config, configure_logging
from permissions.permissions import check_authorization
from service.telegram_service import add_users

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
async def command_start(
        client: Client,
        message: messages_and_media.message.Message):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка на авторизацию bot start')

    if not await check_authorization(message.chat.username):
        await client.send_message(message.chat.id, 'Управлять ботом могут только Администраторы.')
    else:
        await client.send_message(
            message.chat.id,
            f'Здравствуйте, {message.chat.first_name} '
            f' {message.chat.last_name} '
            'Вы авторизованы как администратор бота.',
            reply_markup=keyboard)
        logger.debug('Вы прошли авторизацию как админ бота start!')


        @app.on_message(filters.text == 'начать сбор аналитики')
        async def collect_analitycs(client: Client, message: messages_and_media.message.Message):
            """Обработчик данных кнопки 'начать сбор данных'."""

            logger.info('Бот начал работу')
            await client.send_message(message.chat.id, '...Здесь идет активный сбор данных пользователей...')
            logger.info('...Здесь идет активный сбор данных пользователей...')


@app.on_message(filters.command('add_admin'))
async def command_add_admin(client: Client, message: messages_and_media.message.Message):
    """Обработчик команды на добавление администратора в БД."""

    logger.info('Проверка на авторизацию Cуперпользователя для add_admin')

    if not await check_authorization(message.chat.username, is_superuser=True):
        await client.send_message(
            message.chat.id,
            'У вас недостаточно прав. Добавить администратора может только '
            'суперпользователь.')
    else:
        await client.send_message(
            message.chat.id,
            f'Здравствуйте, {message.chat.first_name} '
            f'{message.chat.last_name}! '
            'Вы авторизованы как суперпользователь.')
        logger.debug('Вы прошли авторизацию как суперпользователь add_admin!')
        await client.send_message(
            message.chat.id,
            'Введите имя пользователя "@123456" в чат.')


@app.on_message(filters.incoming)
async def add_user_db(client: Client, message: messages_and_media.message.Message):
    db_str = await add_users(message.chat.username, message.text)
    print(db_str)
    await client.send_message(
        message.chat.id,
        f'Пользователи {db_str} были добавлены.')


asyncio.run(app.run())
