from enum import Enum
from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from settings import configure_logging
from buttons import inline_bot_2_keyboard
from logic import (
    add_admin, del_admin, auto_generate_report, generate_report, scheduling
)
from permissions.permissions import check_authorization


class Commands(Enum):
    add_admin = 'add_admin_bot_2'
    del_admin = 'del_admin_bot_2'
    auto_report = 'auto_report'
    generate_report = 'generate_report'
    scheduling = 'scheduling'


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
            reply_markup=inline_bot_2_keyboard
        )
        logger.debug(f'{message.chat.username} авторизован!')

        @bot_2.on_callback_query()
        async def report_generation(client: Client, call):
            """Обработчик команд админки бота №2."""

            if call.data == Commands.add_admin.value:
                logger.info('Добавляем администратора')
                await add_admin(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_2_keyboard
                )

            elif call.data == Commands.del_admin.value:
                logger.info('Удаляем администратора')
                await del_admin(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_2_keyboard
                )

            elif call.data == Commands.auto_report.value:
                logger.info('Автоматическое формирование отчёта')
                await auto_generate_report(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_2_keyboard
                )

            elif call.data == Commands.generate_report.value:
                logger.info('Формирование отчёта')
                await generate_report(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_2_keyboard
                )

            elif call.data == Commands.scheduling.value:
                logger.info('Формирование графика')
                await scheduling(client, message)
                await client.send_message(
                    message.chat.id,
                    'Выберите действие:',
                    reply_markup=inline_bot_2_keyboard
                )


if __name__ == '__main__':
    bot_2.run()
