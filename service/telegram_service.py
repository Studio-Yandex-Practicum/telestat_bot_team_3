from core.db import engine, async_session
from crud.userstg import userstg_crud
from permissions.permissions import check_authorization


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
