import os
from dotenv import load_dotenv
from loguru import logger


load_dotenv('.env')


class Config(object):
    """Конфигурация проекта."""

    DB_URI = os.environ['DB_URI']
    API_ID = os.environ['API_ID']
    API_HASH = os.environ['API_HASH']
    BOT_TOKEN = os.environ['BOT_TOKEN']


def configure_logging():
    """Конфигурация логирования проекта."""

    logger.add(
        'logs/file_{time}.log',
        level='DEBUG',
        rotation="50 MB",
        retention="14 days",
        compression="zip",
        enqueue=True
    )
    return logger
