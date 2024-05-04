from enum import Enum
from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from settings import configure_logging
from buttons import bot_2_keyboard
from logic import (
    add_admin, del_admin, auto_generate_report, generate_report, scheduling
)
from permissions.permissions import check_authorization


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    auto_report = 'Автоматическое формирование отчёта'
    generate_report = 'Формирование отчёта'
    scheduling = 'Формирование графика'


logger = configure_logging()
bot_2 = Client("my_account")


@bot_2.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message
):
    """Обработчик команды на запуск бота по формированию отчетов."""

    logger.info('Проверка на авторизацию')

    if False: #not await check_authorization(message.chat.username):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.chat.username}!')
    else:

        await client.send_message(
            message.chat.id, 'Вы прошли авторизацию!',
            reply_markup=bot_2_keyboard
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

            elif message.text == Commands.generate_report.value:
                logger.info('Формирование отчёта')
                await generate_report(client, message)

            elif message.text == Commands.scheduling.value:
                logger.info('Формирование графика')
                await scheduling(client, message)


if __name__ == '__main__':
    bot_2.run()
