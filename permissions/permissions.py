from crud.userstg import userstg_crud
from core.db import engine, async_session


async def check_authorization(user_id=None, username=None, is_superuser=False):
    """Проверка пользователя бота."""

    if user_id is None:
        return False
    async with engine.connect() as session:
        db = await userstg_crud.get_by_attr(
            'user_id',
            user_id,
            session
            )

    if (db is not None and
            user_id == db.user_id and
            db.is_admin and db.is_active):
        if (is_superuser and
                is_superuser == db.is_superuser or
                not is_superuser):
            dbusername = int(db.username) if db.username.isdigit() else db.username
            if username is not None and db.user_id == dbusername:
                async with async_session() as session:
                    async with engine.connect() as session:
                        await userstg_crud.set_update(
                            db.id,
                            {'username': username},
                            session)
            return True
    return False
