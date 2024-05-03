from pyrogram import Client

from core.db import async_session, engine
from crud.userstg import userstg_crud
from permissions.permissions import check_authorization
from settings import configure_logging

logger = configure_logging()


class TelegramGroup():

    def __init__(self, bot: Client, group_name: str):
        self.bot = bot
        self.group_name = group_name

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

    @staticmethod
    async def get_info_chat_user(
        bot: Client,
        group_name: str,
        username: str
    ):
        """"Метод получает информацию о конкретном подписчике чата"""
        await bot.get_chat_member(group_name, username)


async def add_users(username, users=None):
    """Добавление пользователей в ДБ."""

    if not await check_authorization(username, True) or users is None:
        return False

    users = [{'username': user, 'is_superuser': False, 'is_admin': True} for user in users.split(', ')]

    db = ''
    async with async_session() as session:
        async with engine.connect():
            for user in users:
                db += ' ' + (await userstg_crud.create(user, session)).username
    return db


async def get_chat_users(bot: Client, channel: str, filter=None):
    """Метод получения списка подписчиков канала/группы"""
    subsribers = []
    async for subscriber in bot.get_chat_members(channel):
        subsribers.append(subscriber.user.username)
    logger.info(subscriber)
    return subsribers


async def get_chat_members_count(bot: Client, channel: str,):
    return await bot.get_chat_members_count(channel)
