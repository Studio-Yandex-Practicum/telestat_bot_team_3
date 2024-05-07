from pyrogram import Client

from core.db import async_session, engine
from crud.userstg import userstg_crud
from permissions.permissions import check_authorization
from settings import configure_logging
from assistants.assistants import check_by_attr, spy_bot, user_bot

logger = configure_logging()


class ChatUserInfo():
    """Класс для информации о группе/канале"""

    def __init__(
        self,
        bot: Client,
        group_name: str,
        username: str = None
    ):
        self.bot = bot
        self.group_name = group_name
        self.username = username

    async def get_chat(self):
        """Получать объект канала/группы"""
        return await self.bot.get_chat(self.group_name)

    async def get_chat_users(self):
        """Метод получения списка подписчиков канала/группы"""
        subsribers = []
        async for subscriber in self.bot.get_chat_members(self.group_name):
            subsribers.append(subscriber)
        logger.info(subscriber)
        return subsribers

    async def get_chat_members_count(self):
        """Метод получения количества подписчиков канала"""
        members_count = await self.bot.get_chat_members_count(self.group_name)
        logger.info(
            f'@{self.group_name} количество подписчиков: {members_count}'
        )
        return await self.bot.get_chat_members_count(self.group_name)

    async def get_info_chat_user(self):
        """"Метод получает информацию о конкретном подписчике чата"""
        chat_member = await self.bot.get_chat_member(
            self.group_name, self.username
        )
        logger.info(f'Информация об {chat_member.user.username} получена')
        return chat_member

    async def get_full_user_info(self):
        """Формирует список словарей, в которых вся информация о подписчиках"""
        users_info = []
        for user in await self.get_chat_users():
            full_user_info = {}
            full_user_info['ID'] = user.user.id
            full_user_info['Username'] = user.user.username
            full_user_info['Имя'] = user.user.first_name
            full_user_info['Язык пользователя'] = user.user.language_code
            try:
                full_user_info['Дата вступления'] = user.joined_date.strftime('%d-%m-%Y %H:%M:%S')
            except AttributeError:
                full_user_info['Дата вступления'] = 'Отсутствует для владельца'
            full_user_info['Статус подписчика'] = user.status
            full_user_info['Это бот ?'] = 'Да' if user.user.is_bot else 'Нет'
            # try:
            #     full_user_info['Фото'] = await self.bot.download_media(user.user.photo.big_file_id, in_memory=True)
            # except AttributeError:
            #     full_user_info['Фото'] = 'Фото отсутствует'
            users_info.append(full_user_info)
        logger.info('Информация по каждому подписчику собрана')
        return users_info

    @spy_bot
    async def get_chat_messages(self):
        """Возвращает последние 200 сообщений"""
        last_messages = []
        async for message in user_bot.get_chat_history(self.group_name):
            last_messages.append(message)
        logger.info(
            f'Получены последние 200 сообщений из группы {self.group_name}'
        )
        return last_messages

    async def get_activity(self):
        """Возвращает среднее количество просмотров/реакций/репостов"""
        reactions = []
        views = []
        forwards = []
        for activity in await self.get_chat_messages():
            if activity.reactions:
                print(activity.reactions.reactions)
                for reaction in activity.reactions.reactions:
                    logger.info(f'{reaction}')
                    try:
                        reactions.append(reaction.count)
                    except AttributeError:
                        pass
            try:
                forwards.append(activity.forwards)
            except AttributeError:
                pass
            try:
                views.append(activity.views)
            except AttributeError:
                pass
        logger.info(f'{views, reactions, forwards}')
        avg_results = {
            'views': sum(views) / len(views),
            'reactions': sum(reactions) / len(reactions),
            'forwards': sum(forwards) / len(forwards)
        }
        return avg_results


async def add_users(user_id: int,
                    users: list[dict] = None,
                    is_superuser: bool = False,
                    is_admin: bool = True,
                    is_active: bool = True
                    ):
    """Добавление пользователей в ДБ."""

    if not await check_authorization(user_id, True) or users is None:
        return False

    for user in users:
        async with async_session() as session:
            async with engine.connect():
                if await check_by_attr(
                        'user_id',
                        user['user_id'],
                        session
                        ):
                    return False

    users = [{
        'user_id': user['user_id'],
        'username': user['username'],
        'is_superuser': is_superuser,
        'is_admin': is_admin,
        'is_active': is_active
        } for user in users]

    db = ''
    async with async_session() as session:
        async with engine.connect():
            for user in users:
                db += ' ' + (await userstg_crud.create(user, session)).username
    return db


async def del_users():
    """Установка пользователя из ДБ."""

    pass
