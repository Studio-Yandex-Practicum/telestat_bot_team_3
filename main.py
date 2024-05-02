import asyncio

from bot_1 import bot_1
from bot_2 import bot_2
from settings import  configure_logging


logger = configure_logging()


asyncio.run(bot_1.run())
asyncio.run(bot_2.run())
