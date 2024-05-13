from enum import Enum
from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from settings import configure_logging
from buttons import bot_keys
from logic import (
    add_admin, del_admin, auto_generate_report, generate_report, scheduling
)
from permissions.permissions import check_authorization
from assistants.assistants import dinamic_keyboard
from settings import Config


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    auto_report = 'Автоматическое формирование отчёта'
    generate_report = 'Формирование отчёта'
    scheduling = 'Формирование графика'


logger = configure_logging()
bot_2 = Client(
    Config.BOT_ACCOUNT_NAME,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN
)


@bot_2.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message
):
    """Обработчик команды на запуск бота по формированию отчетов."""

    logger.info('Проверка на авторизацию')

    if not await check_authorization(message.chat.username):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.chat.username}!')
    else:

        await client.send_message(
            message.chat.id, 'Вы прошли авторизацию!',
            reply_markup=dinamic_keyboard(
                objs=bot_keys,
                attr_name='key_name',
            )
        )
        logger.debug(f'{message.chat.username} авторизован!')

        @bot_2.on_message()
        async def report_generation(
            client: Client,
            message: messages_and_media.message.Message
        ):
            """Обработчик команд админки бота №2."""

            if message.text == Commands.add_admin.value:
                logger.info('Добавляем администратора')
                await add_admin(client, message)
            elif message.text == Commands.del_admin.value:
                logger.info('Удаляем администратора')
                await del_admin(client, message)

            elif message.text == Commands.auto_report.value:
                logger.info('Автоматическое формирование отчёта')
                await auto_generate_report(client, message)
            ========================
            @bot_1.on_message(filters.regex(Commands.generate_report.value))
            async def generate_report(
                client: Client,
                message: messages_and_media.message.Message
            ):
                """Отправляет отчёт."""

                chat = ChatUserInfo(bot_1, 'vag_angar')
                logger.info('Бот начал работу')
                print(await chat.get_full_user_info())
                await client.send_message(message.chat.id, type(await chat.get_full_user_info()))
            ========================
            elif message.text == Commands.generate_report.value:
                logger.info('Формирование отчёта')
                await generate_report(client, message)

            elif message.text == Commands.scheduling.value:
                logger.info('Формирование графика')
                await scheduling(client, message)


if __name__ == '__main__':
    bot_2.run()
