from service.telegram_service import add_users


async def add_admin(client, message):
    """Добавление администратора(ов) в ДБ."""

    await client.send_message(
        message.chat.id, f'{message.text}...Добавление администратора...'
    )

    # @bot.on_message(filter)
    users = await add_users(user_id=message.chat.id, users_ids=message.text)
    if not users:
        await client.send_message(
            message.chat.id, 'У вас недостаточно прав для добавления '
                             'пользователей или вы ошиблись при вводе '
                             'данных пользователей, пожалуйста добавляйте '
                             'пользовательские id через запятую с пробелом, '
                             'пользовательские id должны быть числами!'
        )
    else:
        await client.send_message(
            message.chat.id, f'Пользователи {users} успешно добавлены.'
        )


async def del_admin(client, message):
    await client.send_message(message.chat.id, '...Удаляем администратора...')


async def choise_channel(client, message):
    await client.send_message(message.chat.id, '...Выбираем телеграм канал...')


async def set_period(client, message):
    await client.send_message(
        message.chat.id, '...Устананвливаем период сбора данных...'
    )


async def auto_generate_report(client, message):
    await client.send_message(
        message.chat.id, '...Автоматическое формирование отчёта...'
    )


async def generate_report(client, message):
    await client.send_message(message.chat.id, '...Формирование отчёта...')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
