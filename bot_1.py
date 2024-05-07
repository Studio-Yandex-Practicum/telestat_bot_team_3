from enum import Enum

from pyrogram import Client, filters
from pyrogram.types import messages_and_media

from buttons import bot_1_keyboard
# from logic import (
#     add_admin,
#     del_admin,
#     choise_channel,
#     generate_report,
#     set_period
# )
from permissions.permissions import check_authorization
from services.telegram_service import add_users, ChatUserInfo
from settings import Config, configure_logging


class Commands(Enum):
    add_admin = 'add_admin'
    del_admin = 'del_admin'
    choise_channel = 'choise_channel'
    set_period = 'set_period'
    generate_report = 'generate_report'


logger = configure_logging()
bot_1 = Client(
    "my_account",
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

    if not await check_authorization(message.chat.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.chat.username}!')
        return
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
            reply_markup=bot_1_keyboard
        )
        logger.debug(f'{message.chat.username} авторизован!')
        return


@bot_1.on_message(filters.regex('add_admin'))
async def command_add_admin(
    client: Client,
    message: messages_and_media.message.Message
):
    """Добавление администратора в ДБ."""

    logger.info('Добавляем администратора')
    await client.send_message(
        message.chat.id, '...Добавление администратора...'
    )
    # users_str = '@Maks_insurance, @jzx659, @XSteelHunterX'
    # users_str = 'sdfsdf'
    users = message.text.split('add_admin ')
    users = await client.get_users(users[1].split(', '))
    users = [{
        'user_id': data.id,
        'username': f'@{data.username}'
        }for data in users]

    users = await add_users(user_id=message.chat.id, users=users)
    if not users:
        await client.send_message(
            message.chat.id, 'У вас недостаточно прав для добавления '
                             'пользователей или вы ошиблись при вводе '
                             'данных пользователей, пожалуйста добавляйте '
                             'пользовательские имена через запятую с пробелом.'
        )
        return
    else:
        await client.send_message(
            message.chat.id, f'Пользователи {users} успешно добавлены.'
        )
        return


@bot_1.on_message(filters.regex(Commands.del_admin.value))
async def command_del_admin(
    client: Client,
    message: messages_and_media.message.Message
):
    """Блокирует администраторов бота в ДБ."""

    logger.info('Блокируем администратора бота')


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


@bot_1.on_message(filters.regex(Commands.choise_channel.value))
async def choise_channel(
    client: Client,
    message: messages_and_media.message.Message
):
    """Находит все каналы владельца."""

    logger.info('Выбираем телеграм канал')


@bot_1.on_message(filters.regex(Commands.set_period.value))
async def set_period(
    client: Client,
    message: messages_and_media.message.Message
):
    """Находит все каналы владельца."""

    logger.info('Устананавливаем период сбора данных')


    #     if message.text == Commands.run_collect_analitics.value:
    #         logger.info('Бот начал работу')
    #         await generate_report(client, message)

    #     elif message.text == 'Добавить администратора':
    #         logger.info('Добавляем администратора')
    #         await add_admin(client, message)

    #     elif message.text == Commands.del_admin.value:
    #         logger.info('Удаляем администратора')
    #         await del_admin(client, message)

    #     elif message.text == Commands.choise_channel.value:
    #         logger.info('Выбираем телеграм канал')
    #         await choise_channel(client, message)

    #     elif message.text == Commands.set_period.value:
    #         logger.info('Устананавливаем период сбора данных')
    #         await set_period(client, message)


if __name__ == '__main__':
    logger.info(' Бот запущен')
    bot_1.run()
