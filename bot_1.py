from enum import Enum

from pyrogram import Client, filters
from pyrogram.types import messages_and_media, ReplyKeyboardRemove

from assistants.assistants import dinamic_ceyboard
from buttons import bot_1_key
from logic import (choise_channel, add_admin, del_admin,
                   run_collect_analitics, set_period, set_channel)
from services.telegram_service import ChatUserInfo
from permissions.permissions import check_authorization
from settings import Config, configure_logging


logger = configure_logging()


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    choise_channel = 'Выбрать телеграм канал'
    set_period = 'Установить период сбора данных'
    run_collect_analitics = 'Начать сбор аналитики'


class BotManager:
    add_admin_flag = False
    del_admin_flag = False
    choise_channel_flag = False
    set_period_flag = False
    chanel = ''
    period = 60


bot_1 = Client(
    'my_account',
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN
)

manager = BotManager()


@bot_1.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка на авторизацию')

    if await check_authorization(message.from_user.id, is_superuser=True):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как владелец!',
            reply_markup=dinamic_ceyboard(
                objs=bot_1_key[:3],
                attr_name='key_name',
                ceyboard_row=2
            )
        )
        logger.debug(f'{message.chat.username} авторизован как владелец!')
    elif await check_authorization(message.from_user.id):
        print(bot_1_key[2])
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как администратор бота!',
            reply_markup=dinamic_ceyboard(
                objs=[bot_1_key[2]],
                attr_name='key_name',
                ceyboard_row=2
            )
        )
        logger.debug(f'{message.chat.username} авторизован как администратор бота!')


@bot_1.on_message(filters.regex(Commands.add_admin.value))
async def command_add_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Добавление администратора в ДБ."""

    if await check_authorization(message.from_user.id):
        logger.info('Добавляем администратора')

        await client.send_message(
            message.chat.id,
            'Укажите никнеймы пользователей, которых хотите добавить '
            'в качестве администраторов, в формате:'
            'nickname1, nickname2, nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.add_admin_flag = True


@bot_1.on_message(filters.regex(Commands.del_admin.value))
async def command_del_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Блокирует администраторов бота в ДБ."""

    if await check_authorization(message.from_user.id):
        logger.info('Блокируем администратора бота')
        await client.send_message(
            message.chat.id,
            'Укажите никнеймы администраторов, которых хотите деактивировать, '
            'в формате nickname1, nickname2, nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.del_admin_flag = True


@bot_1.on_message(filters.regex(Commands.run_collect_analitics.value))
async def generate_report(
    client: Client,
    message: messages_and_media.message.Message
):
    """Отправляет отчёт."""

    chat = ChatUserInfo(bot_1, 'vag_angar')
    logger.info('Бот начал работу')
    info = await chat.create_report()
    await client.send_message(message.chat.id, len(info))


@bot_1.on_message(filters.regex(Commands.choise_channel.value))
async def choise_channel_cmd(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Находит все каналы владельца."""

    logger.info('Выбираем телеграм канал')
    if await check_authorization(message.from_user.id):
        await choise_channel(client, message)
        manager.choise_channel_flag = True


@bot_1.on_message(filters.regex(Commands.set_period.value))
async def set_period_cmd(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Устанавливает переиод сбора данных."""

    logger.info('Устананавливаем период сбора данных')
    if await check_authorization(message.from_user.id):
        await set_period(client, message)
        manager.set_period_flag = True
        await client.send_message(
            message.chat.id,
            'Для запуска сбора статистики нажмите кнопку.',
            reply_markup=dinamic_ceyboard(
                objs=[bot_1_key[4]],
                attr_name='key_name',
                ceyboard_row=2
            )
        )


@bot_1.on_message(filters.regex(Commands.run_collect_analitics.value))
async def run_collect_cmd(
    client: Client,
    message: messages_and_media.message.Message
):
    """Производит сбор данных в канале/группе."""

    logger.info('Начинаем сбор данных')
    if await check_authorization(message.from_user.id):
        await run_collect_analitics(client, message)


@bot_1.on_message()
async def all_incomming_messages(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Здесь обрабатываем все входящие сообщения."""

    if manager.add_admin_flag:
        await add_admin(client, message)
        manager.add_admin_flag = False

    if manager.del_admin_flag:
        await del_admin(client, message)
        manager.del_admin_flag = False

    if manager.choise_channel_flag:
        channels = await set_channel()
        channel_name = ''
        for channel in channels.chats:
            if channel.username == message.text:
                channel_name = f'@{message.text}'
                logger.info(f'Найден канал: {channel_name}')
                break

        manager.choise_channel_flag = False
        manager.chanel = channel_name

        await client.send_message(
            message.chat.id,
            'Выберете периодичность сбора аналитики.',
            reply_markup=dinamic_ceyboard(
                objs=bot_1_key[3:],
                attr_name='key_name',
                ceyboard_row=2
            )
        )

    if manager.set_period_flag:
        print('Здесь должна быть функция выбора периодичности')
        period = 60  # например 60 минут
        await client.send_message(
            message.chat.id,
            'Для запуска сбора статистики нажмите кнопку.',
            reply_markup=dinamic_ceyboard(
                objs=[bot_1_key[4]],
                attr_name='key_name',
                ceyboard_row=2
            )
        )
        manager.period = period
        manager.set_period_flag = False


if __name__ == '__main__':
    logger.info(' Бот запущен')
    bot_1.run()
