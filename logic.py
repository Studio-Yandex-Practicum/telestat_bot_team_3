from services.telegram_service import add_users, ChatUserInfo
from permissions.permissions import check_authorization
from typing import Literal
from settings import configure_logging


logger = configure_logging()


async def manage_admin(client, message, action: Literal['add', 'del']):
    action_values = {
        'add': {
            'split_str': 'add_admin ',
            'msg_str': 'добавления',
            'done_msg_str': 'добавлены',

        },
        'del': {
            'split_str': 'del_admin ',
            'msg_str': 'удаления',
            'done_msg_str': 'удалены'
        },
    }
    # users_str = '@Maks_insurance, @jzx659, @XSteelHunterX'
    # users_str = 'sdfsdf'
    users = message.text.split(action_values[action]['split_str'])
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
                             'пользовательские имена через запятую с пробелом.'
        )
        return
    else:
        await client.send_message(
            message.chat.id, f'Пользователи {users} успешно {action_values[action]["done_msg_str"]}.'
        )
        return


async def is_admin(client, message):
    if not await check_authorization(message.chat.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
        logger.info(f'Неудачная авторизация {message.chat.username}!')
        return False
    return True


async def add_admin(client, message):
    """Добавление администратора(ов) в ДБ."""

    await client.send_message(
        message.chat.id, '...Добавление администратора...'
    )
    await manage_admin(client, message, action='add')


async def del_admin(client, message):
    await client.send_message(message.chat.id, '...Удаляем администратора...')
    await manage_admin(client, message, action='del')


async def choise_channel(client, message):
    await client.send_message(message.chat.id, '...Выбираем телеграм канал...')


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
    print(await chat.get_full_user_info())
    await client.send_message(message.chat.id, type(await chat.get_full_user_info()))


async def generate_report(client, message):
    await client.send_message(message.chat.id, '...Формирование отчёта...')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
