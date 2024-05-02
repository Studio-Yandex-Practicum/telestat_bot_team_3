import asyncio

from bot_1 import bot_1
from bot_2 import bot_2
from settings import  configure_logging
from core.base import Base
from core.db import engine


logger = configure_logging()


# async def init_models():
#     """Для проверки создаём таблицу в ручную."""

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_models())


asyncio.run(bot_1.run())
# asyncio.run(bot_2.run())
