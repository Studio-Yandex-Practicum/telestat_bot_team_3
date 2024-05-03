from service.telegram_service import TelegramGroup, get_chat_users, get_chat_members_count


async def add_admin(client, message):
    await client.send_message(
        message.chat.id, '...Добавление администратора...'
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
    chat = TelegramGroup(client, 'telestat_team')
    await client.send_message(message.chat.id, await TelegramGroup.get_info_chat_user(client, 'telestat_team', 'Maks_insurance'))


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
