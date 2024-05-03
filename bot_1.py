from enum import Enum
from typing import Union

from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from buttons import bot_1_keyboard
from logic import add_admin, choise_channel, del_admin, set_period
from permissions.permissions import check_authorization
from settings import Config, configure_logging


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    choise_channel = 'Выбрать телеграм канал'
    set_period = 'Установить период сбора данных'


logger = configure_logging()
bot_1 = Client(
    'my_account',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN)


@bot_1.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка на авторизацию')

    if not await check_authorization(message.chat.username):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.chat.username}!')
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
            reply_markup=bot_1_keyboard
        )
        logger.debug(f'{message.chat.username} авторизован!')

        @bot_1.on_message()
        async def collect_analitycs(
            client: Client,
            message: messages_and_media.message.Message
        ):
            """Обработчик команд админки бота №1."""

            if message.text == 'Начать сбор аналитики':
                logger.info('Бот начал работу')
                await client.send_message(
                    message.chat.id,
                    '...Здесь идет активный сбор данных пользователей...'
                )

            elif message.text == Commands.add_admin.value:
                logger.info('Добавляем администратора')
                await add_admin(client, message)

            elif message.text == Commands.del_admin.value:
                logger.info('Удаляем администратора')
                await del_admin(client, message)

            elif message.text == Commands.choise_channel.value:
                logger.info('Выбираем телеграм канал')
                await choise_channel(client, message)

            elif message.text == Commands.set_period.value:
                logger.info('Устананвливаем период сбора данных')
                await set_period(client, message)

        await collect_analitycs(client, message)


if __name__ == '__main__':
    bot_1.run()
