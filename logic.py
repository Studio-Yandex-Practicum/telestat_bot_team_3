
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
    await client.send_message(message.chat.id, '...Формирование отчёта...')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
