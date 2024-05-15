from typing import Literal

from pyrogram.errors.exceptions.bad_request_400 import (ChatAdminRequired,
                                                        UsernameInvalid,
                                                        UsernameNotOccupied,
                                                        UserNotParticipant)
from pyrogram.errors.exceptions.flood_420 import FloodWait

from assistants.assistants import dinamic_keyboard
from buttons import bot_keys
from services.google_api_service import get_report
from services.telegram_service import (ChatUserInfo, add_users, get_channels,
                                       update_users)
from settings import Config, configure_logging

logger = configure_logging()


async def manage_admin(client, message, act: Literal['add', 'del']):
    action = {
        'add': {
            't1': 'Добавляются',
            'msg_str': 'добавлении',
            'done_msg_str': 'добавлены',
        },
        'del': {
            't1': 'Удаляются',
            'msg_str': 'удалении',
            'done_msg_str': 'удалены',
        },
    }
    cur_msg_str = action[act]['msg_str']
    cur_t1 = action[act]['t1']
    cur_done = action[act]['done_msg_str']

    try:
        incom_users = await client.get_users(message.text.split(', '))
    except UsernameInvalid as error:
        logger.error(
            f'Ошибка при {cur_msg_str} админов {message.text}\n {error}'
        )
        await client.send_message(
            message.chat.id,
            f'Проверьте корректность написания пользователей {message.text}',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[:3],
                attr_name='key_name',
                keyboard_row=2
            )
        )
    except UsernameNotOccupied as error:
        logger.error(
            f'ошибка при {cur_msg_str} админов {message.text}\n {error}'
        )
        await client.send_message(
            message.chat.id,
            f'Проверьте правильность написания никнеймов {message.text}, '
            'один из никнеймов не существует',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[:3],
                attr_name='key_name',
                keyboard_row=2
            )
        )
    else:
        if act == 'del':
            logger.info(f'{cur_t1} администраторы {message.text}')
            deactivate_admins = [
                {
                    'user_id': user.id,
                    'username': user.username
                } for user in incom_users
            ]
            await update_users(
                user_id=message.from_user.id,
                users=deactivate_admins,
                is_active=False
            )
        else:
            logger.info(f'{cur_t1} администраторы {message.text}')
            added_admins = [
                {
                    'user_id': user.id,
                    'username': user.username
                } for user in incom_users
            ]
            await add_users(
                user_id=message.from_user.id,
                users=added_admins,
                is_superuser=False,
                is_admin=True,
                is_active=True
            )
            await client.send_message(
                message.chat.id,
                f'Администраторы {message.text} успешно {cur_done}.',
                reply_markup=dinamic_keyboard(
                    objs=bot_keys[:3],
                    attr_name='key_name',
                    keyboard_row=2
                )
            )
            logger.info(
                f'Администраторы {message.text} успешно {cur_done}'
            )


async def add_admin(client, message):
    """Добавление администратора(ов) в ДБ."""

    await manage_admin(client, message, act='add')


async def del_admin(client, message):
    """Деактивация администратора(ов) в ДБ."""

    await manage_admin(client, message, act='del')


async def choise_channel(client, message):
    """Получение каналов и выбор неоходимого канала телеграм."""

    channels = []
    for channel in await get_channels():
        try:
            (await client.get_chat_member(
                channel.chat.username, Config.BOT_ACCOUNT_NAME))
            channels.append(channel.chat)
        except FloodWait as e:
            logger.error(f'У пользователя {Config.USER_ACCOUNT_NAME} '
                         'слишком много контактов, сработала защита '
                         f'"Телеграм"/n {e}')
        except ChatAdminRequired:
            logger.error(f'Пользователю: {Config.BOT_ACCOUNT_NAME} '
                         'требуются права администратора.')
        except UserNotParticipant:
            logger.error(f'Пользователь: {Config.BOT_ACCOUNT_NAME} '
                         'не является владельцем канала.')
    if channels:
        await client.send_message(
            message.chat.id,
            'Выберете желаемый канал на клавиатуре, при его отсутствии '
            'введите канал вручную.',
            reply_markup=dinamic_keyboard(
                objs=channels,
                attr_name='username',
                keyboard_row=4
                )
            )
        return channels
    else:
        await client.send_message(
            message.chat.id,
            'Вероятно вы не являетесь владельцем ниодного канала! '
            'Заведите свои каналы или введите требуемый канал '
            'в текстовое поле и если "Бот" в нём зарегистрирован '
            'продолжайте работу с "Ботом.',
            reply_markup=dinamic_keyboard(
                objs=[bot_keys[2]],
                attr_name='key_name'
                )
            )
    return False


async def run_collect_analitics(client, message):
    await client.send_message(
        message.chat.id, '...Начинаем сбор данных...'
    )


async def auto_generate_report(client, message, bot_1):
    await client.send_message(
        message.chat.id, '...Автоматическое формирование отчёта...'
    )
    chat = ChatUserInfo(bot_1, 'vag_angar')
    logger.info('Бот начал работу')
    report = await chat.create_report()
    await get_report(report)
    await client.send_message(message.chat.id, type(await chat.create_report()))


async def generate_report(client, message):
    await client.send_message(message.chat.id, '...Формирование отчёта...')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
