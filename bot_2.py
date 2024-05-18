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
    Config.BOT2_ACCOUNT_NAME,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT2_TOKEN
)


class BotManager:
    """Конфигурация глобальных настроек бота."""
    add_admin_flag = False
    del_admin_flag = False
    choise_channel_flag = False
    set_period_flag = False
    stop_channel_flag = True
    owner_or_admin = ''
    chanel = ''
    period = 10
    work_period = 60


manager = BotManager()


@bot_2.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка авторизации.')

    if await check_authorization(message.from_user.id, is_superuser=True):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как владелец!',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[:3] + bot_keys[14:15],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'owner'
        logger.debug(f'{message.chat.username} авторизован как владелец!')
    elif await check_authorization(message.from_user.id):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как администратор бота!',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[2:3] + bot_keys[14:15],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'admin'
        logger.debug(
            f'{message.chat.username} авторизован как администратор бота!'
            )



        # @bot_2.on_message()
        # async def report_generation(
        #     client: Client,
        #     message: messages_and_media.message.Message
        # ):
        #     """Обработчик команд админки бота №2."""

        #     if message.text == Commands.add_admin.value:
        #         logger.info('Добавляем администратора')
        #         await add_admin(client, message)
        #     elif message.text == Commands.del_admin.value:
        #         logger.info('Удаляем администратора')
        #         await del_admin(client, message)

        #     elif message.text == Commands.auto_report.value:
        #         logger.info('Автоматическое формирование отчёта')
        #         await auto_generate_report(client, message)

        #     @bot_1.on_message(filters.regex(Commands.generate_report.value))
        #     async def generate_report(
        #         client: Client,
        #         message: messages_and_media.message.Message
        #     ):
        #         """Отправляет отчёт."""

        #         chat = ChatUserInfo(bot_1, 'vag_angar')
        #         logger.info('Бот начал работу')
        #         print(await chat.get_full_user_info())
        #         await client.send_message(message.chat.id, type(await chat.get_full_user_info()))

        #     elif message.text == Commands.generate_report.value:
        #         logger.info('Формирование отчёта')
        #         await generate_report(client, message)

        #     elif message.text == Commands.scheduling.value:
        #         logger.info('Формирование графика')
        #         await scheduling(client, message)


if __name__ == '__main__':
    logger.info('Bot 2 started.')
    bot_2.run()
