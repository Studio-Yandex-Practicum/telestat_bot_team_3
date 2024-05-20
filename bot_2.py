from enum import Enum
import re
from pyrogram import Client, filters
from pyrogram.types import messages_and_media, ReplyKeyboardRemove

from settings import configure_logging
from buttons import bot_keys
from logic import (
    add_admin, del_admin, auto_report, generate_report, scheduling
)
from permissions.permissions import check_authorization
from assistants.assistants import dinamic_keyboard
from settings import Config
from services.google_api_service import get_report


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
    choise_report_flag = False
    choise_auto_report_flag = False
    scheduling_flag = False
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
                objs=bot_keys[:2] + bot_keys[5:8],
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
                objs=bot_keys[5:8],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'admin'
        logger.debug(
            f'{message.chat.username} авторизован как администратор бота!'
            )


@bot_2.on_message(filters.regex(Commands.add_admin.value))
async def command_add_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Добавление администратора в ДБ."""

    if manager.owner_or_admin == 'owner':
        logger.info('Добавляем администратора')

        await client.send_message(
            message.chat.id,
            'Укажите никнеймы пользователей, которых хотите добавить '
            'в качестве администраторов, в формате: '
            '@nickname1, @nickname2, @nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.add_admin_flag = True


@bot_2.on_message(filters.regex(Commands.del_admin.value))
async def command_del_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Блокирует администраторов бота в ДБ."""

    if manager.owner_or_admin == 'owner':
        logger.info('Блокируем администратора(ов) бота')
        await client.send_message(
            message.chat.id,
            'Укажите никнеймы администраторов, которых хотите деактивировать, '
            'в формате @nickname1, @nickname2, @nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.del_admin_flag = True


@bot_2.on_message(filters.regex(Commands.generate_report.value))
async def command_generate_report(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Создаёт отчёт вручную."""

    await generate_report(client, message)
    manager.choise_report_flag = True


@bot_2.on_message(filters.regex(Commands.auto_report.value))
async def command_auto_report(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Создаёт отчёт автоматически."""

    await auto_report(client, message)
    manager.choise_auto_report_flag = True


@bot_2.on_message(filters.regex(Commands.scheduling.value))
async def command_sheduling(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Создаёт графики."""

    await auto_report(client, message)
    manager.scheduling_flag = True


@bot_2.on_message()
async def all_incomming_messages(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Здесь обрабатываем все входящие сообщения."""

    if manager.add_admin_flag:
        await add_admin(client, message)
        manager.add_admin_flag = False

    elif manager.del_admin_flag:
        await del_admin(client, message)
        manager.del_admin_flag = False
    elif manager.choise_report_flag:
        logger.info('Приняли команду на формирование отчёта')
        manager.choise_report_flag = False
    elif manager.choise_auto_report_flag:
        logger.info('Приняли команду на aвтоматическое формирование отчёта')
        manager.choise_auto_report_flag = False
    elif manager.scheduling_flag:
        logger.info('Приняли команду на создание графика.')
        manager.scheduling_flag = False
    else:
        await client.send_message(
            message.chat.id,
            'Упс, этого действия мы от вас не ожидали! \n'
            'Или вы пытаетесь выполнить действие на которое '
            'у вас нет прав, "Авторизуйтесь", командой: /start'
        )
        manager.owner_or_admin = ''


if __name__ == '__main__':
    logger.info('Bot 2 is started.')
    bot_2.run()
