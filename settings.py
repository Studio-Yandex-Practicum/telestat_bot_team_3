import os

from dotenv import load_dotenv
from loguru import logger


load_dotenv('.env')


class Config(object):
    """Конфигурация проекта."""

    DB_URI = os.environ['DB_URI']


def configure_logging():
    logger.add(
        'logs/file_{time}.log',
        level='DEBUG',
        rotation="50 MB",
        retention="14 days",
        compression="zip",
        enqueue=True
    )
    return logger
