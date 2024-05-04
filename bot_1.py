from enum import Enum
from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from settings import configure_logging
from buttons import bot_1_keyboard
from logic import add_admin, del_admin, choise_channel, set_period
from permissions.permissions import check_authorization
from buttons2 import inline_bot_1_keyboard
# from pyrogram.types import Remove

# class Commands(Enum):
#     add_admin = 'Добавить администратора'
#     del_admin = 'Удалить администратора'
#     choise_channel = 'Выбрать телеграм канал'
#     set_period = 'Установить период сбора данных'

class Commands(Enum):
    add_admin = 'add_admin_bot_1'
    del_admin = 'del_admin_bot_1'
    choise_channel = 'choise_channel'
    set_period = 'set_period'
    run_collect_analitics = 'run_collect_analitics'


logger = configure_logging()
bot_1 = Client("my_account")


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
            reply_markup=inline_bot_1_keyboard
        )
        logger.debug(f'{message.chat.username} авторизован!')

        @bot_1.on_callback_query()
        async def collect_analitycs(client: Client, call):
            """Обработчик команд админки бота №1."""

            if call.data == Commands.run_collect_analitics.value:
                logger.info('Бот начал работу')
                await client.send_message(
                    message.chat.id,
                    '...Здесь идет активный сбор данных пользователей...'
                )

            elif call.data == Commands.add_admin.value:
                logger.info('Добавляем администратора')
                await add_admin(client, message)
                message_id = await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_1_keyboard
                )
                # await client.send_message(
                #     message.chat.id,
                #     message_id.id,
                #     reply_markup=inline_bot_1_keyboard
                # )
                await client.delete_messages(
                    message_ids=message_id.id,
                    chat_id=message.chat.id
                )

            elif call.data == Commands.del_admin.value:
                logger.info('Удаляем администратора')
                await del_admin(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_1_keyboard
                )

            elif call.data == Commands.choise_channel.value:
                logger.info('Выбираем телеграм канал')
                await choise_channel(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_1_keyboard
                )

            elif call.data == Commands.set_period.value:
                logger.info('Устананавливаем период сбора данных')
                await set_period(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_1_keyboard
                )


if __name__ == '__main__':
    bot_1.run()
