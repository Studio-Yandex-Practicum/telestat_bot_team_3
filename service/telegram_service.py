from pyrogram import Client

from core.db import async_session, engine
from crud.userstg import userstg_crud
from permissions.permissions import check_authorization
from settings import configure_logging

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
            subsribers.append(subscriber.user.username)
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

    # async def get_chat_messages(self):
    #     """Возвращает последние 200 сообщений"""
    #     last_messages = await self.bot.get_messages(self.group_name)
    #     logger.info(
    #         f'Получены последние 200 сообщений из группы {self.group_name}'
    #     )
    #     return last_messages


async def add_users(username, users=None):
    """Добавление пользователей в ДБ."""

    if not await check_authorization(username, True) or users is None:
        return False

    users = [{'username': user, 'is_superuser': is_superuser, 'is_admin': True, 'is_active': is_active} for user in users.split(', ')]

    db = ''
    async with async_session() as session:
        async with engine.connect():
            for user in users:
                db += ' ' + (await userstg_crud.create(user, session)).username
    return db


async def del_users():
    """Установка пользователя из ДБ."""
    pass
