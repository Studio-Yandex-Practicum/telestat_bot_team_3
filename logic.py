from typing import Literal

from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from permissions.permissions import check_authorization
from services.telegram_service import ChatUserInfo, add_users, get_channels
from settings import configure_logging

logger = configure_logging()


async def manage_admin(client, message, action: Literal['add', 'del']):
    action_values = {
        'add': {
            'split_str': 'add_admin ',
            'msg_str': 'добавления',
            'done_msg_str': 'добавлены',
            'cmd_msg_str': 'Добавить администратора',

        },
        'del': {
            'split_str': 'del_admin ',
            'msg_str': 'удаления',
            'done_msg_str': 'удалены',
            'cmd_msg_str': 'Удалить администратора',
        },
    }
    # users_str = '@Maks_insurance, @jzx659, @XSteelHunterX'
    # users_str = 'sdfsdf'
    delimiter = action_values[action]['split_str']
    if not message.text.startswith(delimiter):
        await client.send_message(
            message.chat.id,
            f'Сообщение должно начинатьтся с команды {delimiter}.\n'
            f'Формат сообщения: \n{delimiter} @username1, @username2\n'
            'После написания команды необходимо нажать кнопку '
            f'{action_values[action]["cmd_msg_str"]}'
        )
        return
    users = message.text.split(delimiter)
    users = await client.get_users(users[1].split(', '))
    users = [{
        'user_id': data.id,
        'username': f'@{data.username}'
        }for data in users]
    args = {
        'user_id': message.chat.id,
        'users': users
    }
    if action == 'del':
        args.update({'is_active': False})
    users = await add_users(*args)
    if not users:
        await client.send_message(
            message.chat.id, f'У вас недостаточно прав для {action_values[action]["msg_str"]} '
                             'пользователей или вы ошиблись при вводе '
                             'данных пользователей, пожалуйста добавляйте '
                             'имена пользователей через запятую с пробелом.'
        )
        return
    else:
        await client.send_message(
            message.chat.id, f'Пользователи {users} успешно {action_values[action]["done_msg_str"]}.'
        )
        return


async def is_admin(client, message):
    """Проверка авторизации."""

    if not await check_authorization(message.from_user.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.from_user.username}!')
        return False
    return True


async def add_admin(client, message):
    """Добавление администратора(ов) в ДБ."""
    await manage_admin(client, message, action='add')


async def del_admin(client, message):
    await manage_admin(client, message, action='del')


async def choise_channel(client, message, bot):
    """Получение каналов и выбор неоходимого канала телеграм."""

    await client.send_message(message.chat.id, '...Выбираем телеграм канал...')
    channels = await get_channels()
    print(len(channels.chats))
    btn_1_4 = []
    btn_many = []
    counter = 1
    for chat in channels.chats:
        print(chat.username)
        if counter > 0:
            counter -= 1
            btn_1_4.append(KeyboardButton(text=f'@{chat.username}'))
        else:
            counter = 1
            btn_1_4.append(KeyboardButton(text=f'@{chat.username}'))
            btn_many.append(btn_1_4)

    if btn_many:
        channels_btn = ReplyKeyboardMarkup(keyboard=[
            btn_1_4
        ], resize_keyboard=True)
    else:
        channels_btn = ReplyKeyboardMarkup(keyboard=btn_many, resize_keyboard=True)

    # channels_btn = ReplyKeyboardMarkup(keyboard=[
    #     [
    #         KeyboardButton(text='Добавить'),
    #         KeyboardButton(text='Удалить'),
    #     ],
    # ], resize_keyboard=True)


    # await client.send_message(message.chat.id, 'Меняем клаву', reply_markup=ReplyKeyboardRemove())
    await client.send_message(
        message.chat.id,
        'Выберете желаемый из своих каналов на клавиатуре.',
        reply_markup=channels_btn
    )
    print(channels_btn)
    return


async def set_period(client, message):
    await client.send_message(
        message.chat.id, '...Устананвливаем период сбора данных...'
    )


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
    print(await chat.create_report())
    await client.send_message(message.chat.id, type(await chat.create_report()))


async def generate_report(client, message):
    await client.send_message(message.chat.id, '...Формирование отчёта...')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
