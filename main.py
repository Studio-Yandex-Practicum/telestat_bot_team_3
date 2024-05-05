import asyncio

from bot_1 import bot_1
# from bot_2 import bot_2
from settings import configure_logging
from services.launcher import init_process
import logging
logging.basicConfig(level=logging.INFO)
# from core.base import Base
# from core.db import engine


logger = configure_logging()


# async def init_models():
#     """Для проверки создаём таблицу в ручную."""

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


loop = asyncio.get_event_loop()
loop.run_until_complete(init_process())
loop.run_forever(bot_1.run())
