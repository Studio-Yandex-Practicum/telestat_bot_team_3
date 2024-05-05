from core.db import async_session, engine
from crud.userstg import userstg_crud
from permissions.permissions import check_authorization


async def add_users(user_id,
                    users_ids=None,
                    is_superuser=False,
                    is_active=True):
    """Добавление пользователей в ДБ."""

    if (not await check_authorization(user_id, is_superuser=is_superuser) or
            users_ids is None):
        return False

    users = [{'user_id': int(user_id) if user_id.isdigit() else 0,
              'username': user_id,
              'is_superuser': is_superuser,
              'is_admin': True,
              'is_active': is_active
              } for user_id in users_ids.split(', ')]

    for user in users:
        if user['user_id'] == 0:
            return False

    db = ''
    async with async_session() as session:
        async with engine.connect():
            for user_id in users_ids:
                db += ' ' + (
                    await userstg_crud.create(
                        user_id, session)).username
    return db


async def del_users():
    """Установка пользователя из ДБ."""
    pass
