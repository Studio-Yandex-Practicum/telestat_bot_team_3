import asyncio
import logging
import subprocess
from threading import Thread

from bot_1 import bot_1
from bot_2 import bot_2
from services.launcher import init_process
from settings import configure_logging

logging.basicConfig(level=logging.INFO)
# from core.base import Base
# from core.db import engine


logger = configure_logging()


# async def init_models():
#     """Для проверки создаём таблицу в ручную."""

#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


# init_process()

# subprocess.Popen('python bot_1.py')
# subprocess.Popen('python bot_2.py')

# pool = mp.Pool(mp.cpu_count())
# pool.apply_async(bot_1.run())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot_2.run())
# loop.run_forever()

# pool = mp.Pool(mp.cpu_count())
# def run_command():
#     subprocess.run(bot_1.run())
#     subprocess.run(bot_2.run())


if __name__ == '__main__':

    import multiprocessing as mp
    import subprocess
    from threading import Thread

    Thread(target=subprocess.run, args=['py bot_1.py']).start()
    Thread(target=subprocess.run, args=['py bot_2.py']).start()
