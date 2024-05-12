from enum import Enum

from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from assistants.assistants import dinamic_keyboard
from buttons import bot_1_key
from logic import (add_admin, choise_channel, del_admin, is_admin,
                   run_collect_analitics, set_period, set_channel)
from services.telegram_service import ChatUserInfo
from settings import Config, configure_logging

logger = configure_logging()


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    choise_channel = 'Выбрать телеграм канал'
    set_period = 'Установить период сбора данных'
    run_collect_analitics = 'Начать сбор аналитики'


bot_1 = Client(
    'my_account',
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN
)


@bot_1.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка на авторизацию')

    if await is_admin(client, message, is_superuser=True):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как владелец!',
            reply_markup=dinamic_keyboard(
                objs=bot_1_key[:3],
                attr_name='key_name',
                ceyboard_row=2
            )
        )
        logger.debug(f'{message.chat.username} авторизован как владелец!')
    elif await is_admin(client=client, message=message):
        print(bot_1_key[2])
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как администратор бота!',
            reply_markup=dinamic_keyboard(
                objs=[bot_1_key[2]],
                attr_name='key_name',
                ceyboard_row=2
            )
        )
        logger.debug(f'{message.chat.username} авторизован как администратор бота!')


@bot_1.on_message(filters.regex(Commands.add_admin.value))
async def command_add_admin(
    client: Client,
    message: messages_and_media.message.Message
):
    """Добавление администратора в ДБ."""

    logger.info('Добавляем администратора')
    if await is_admin(client, message):
        await add_admin(client, message)


@bot_1.on_message(filters.regex(Commands.del_admin.value))
async def command_del_admin(
    client: Client,
    message: messages_and_media.message.Message
):
    """Блокирует администраторов бота в ДБ."""

    logger.info('Блокируем администратора бота')


@bot_1.on_message(filters.regex(Commands.run_collect_analitics.value))
async def generate_report(
    client: Client,
    message: messages_and_media.message.Message
):
    """Отправляет отчёт."""

    chat = ChatUserInfo(bot_1, 'vag_angar')
    logger.info('Бот начал работу')
    info = await chat.create_report()
    print(info)
    await client.send_message(message.chat.id, len(info))


@bot_1.on_message(filters.regex(Commands.choise_channel.value))
async def choise_channel_cmd(
    client: Client,
    message: messages_and_media.message.Message
):
    """Находит все каналы владельца."""

    logger.info('Выбираем телеграм канал')
    if await is_admin(client, message):
        await choise_channel(client, message, bot=bot_1)


@bot_1.on_message(filters.regex(Commands.set_period.value))
async def set_period_cmd(
    client: Client,
    message: messages_and_media.message.Message
):
    """Устанавливает переиод сбора данных."""

    logger.info('Устананавливаем период сбора данных')
    if await is_admin(client, message):
        await set_period(client, message)


@bot_1.on_message(filters.regex(Commands.run_collect_analitics.value))
async def run_collect_cmd(
    client: Client,
    message: messages_and_media.message.Message
):
    """Производит сбор данных в канале/группе."""

    logger.info('Начинаем сбор данных')
    if await is_admin(client, message):
        await run_collect_analitics(client, message)


@bot_1.on_message()
async def all_incomming_messages(
    client: Client,
    message: messages_and_media.message.Message
):
    """Здесь обрабатываем все входящие сообщения."""

    channels = await set_channel()

    channel_name = ''
    for channel in channels.chats:
        if channel.username == message.text:
            channel_name = f'@{message.text}'
            logger.info(f'Найден канал: {channel_name}')
            break



if __name__ == '__main__':
    logger.info(' Бот запущен')
    bot_1.run()
