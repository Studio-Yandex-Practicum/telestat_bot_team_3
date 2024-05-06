from functools import wraps

from pyrogram import Client

from crud.userstg import userstg_crud
from settings import Config, logger


user_bot = Client(
    'my_account2',
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    phone_number=Config.PHONE_NUMBER
)


async def check_by_attr(attr_name, attr_value, session) -> bool:
    """Проверка id на наличие в ДБ."""

    if await userstg_crud.get_by_attr(
            attr_name,
            attr_value,
            session
            ) is None:
        return False
    return True


def spy_bot(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await user_bot.start()
        logger.info('Шпион запущен')
        try:
            result = await func(*args, **kwargs)
            logger.info('Данные получены')
            return result
        finally:
            await user_bot.stop()
            logger.info('Шпион ускользнул')
    return wrapper
