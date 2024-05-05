from datetime import datetime

from service.telegram_service import ChatUserInfo


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
    chat = ChatUserInfo(client, 'telestat_team')
    parse_info = {
        'Название канала/группы': chat.group_name,
        'Дата и время отчета': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'Количество подписчиков': await chat.get_chat_members_count(),
        'Полная информация о пользователях': await chat.get_full_user_info()
    }
    # messages = await chat.get_chat_messages()
    # for message in messages:
    #     print(message)
    print(parse_info)
    await client.send_message(message.chat.id, 'Данные сформированы в словарь')


async def scheduling(client, message):
    await client.send_message(message.chat.id, '...Формирование графика...')
