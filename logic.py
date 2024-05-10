from typing import Literal

from permissions.permissions import check_authorization
from services.telegram_service import ChatUserInfo, add_users, get_channels
from settings import configure_logging
from assistants.assistants import dinamic_ceyboard

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

    await client.send_message(
        message.chat.id,
        'Выберете желаемый из своих каналов на клавиатуре.',
        reply_markup=dinamic_ceyboard(
            objs=channels.chats,
            attr_name='username',
            ceyboard_row=4
            )
        )
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
