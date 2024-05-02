from crud.userstg import userstg_crud
from core.db import engine


async def check_authorization(username=None, is_superuser=False):
    """Проверка пользователя бота."""

    if username is None:
        return False

    async with engine.connect() as session:
        db = await userstg_crud.get_by_attr(
            'username',
            username,
            session
            )

    if username == db.username and db.is_admin and db.is_active:
        if (is_superuser and
                is_superuser == db.is_superuser or
                not is_superuser):
            return True
    return False
