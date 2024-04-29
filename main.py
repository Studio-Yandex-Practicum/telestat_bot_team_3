import asyncio

from core.db import engine
from models.userstg import UsersTG


async def init_models():
    """Для проверки создаём таблицу в ручную."""

    async with engine.begin() as conn:
        await conn.run_sync(UsersTG.metadata.drop_all)
        await conn.run_sync(UsersTG.metadata.create_all)

asyncio.run(init_models())
