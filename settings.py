import os

from dotenv import load_dotenv
from loguru import logger
from loguru._logger import Logger


load_dotenv('.env')


class Config(object):
    """Конфигурация проекта."""

    DB_URI = os.environ['DB_URI']
    API_ID = os.environ['API_ID']
    API_HASH = os.environ['API_HASH']
    BOT_TOKEN = os.environ['BOT_TOKEN']

    # Конфигурация для гугл таблиц
    TYPE = os.environ['TYPE']
    PROJECT_ID = os.environ['PROJECT_ID']
    PRIVATE_KEY_ID = os.environ['PRIVATE_KEY_ID']
    PRIVATE_KEY = os.environ['PRIVATE_KEY']
    CLIENT_EMAIL = os.environ['CLIENT_EMAIL']
    CLIENT_ID = os.environ['CLIENT_ID']
    AUTH_URI = os.environ['AUTH_URI']
    TOKEN_URI = os.environ['TOKEN_URI']
    AUTH_PROVIDER_X509_CERT_URL = os.environ['AUTH_PROVIDER_X509_CERT_URL']
    CLIENT_X509_CERT_URL = os.environ['CLIENT_X509_CERT_URL']
    EMAIL = os.environ['EMAIL']


def configure_logging() -> Logger:
    """
    Функция-конфигуратор логгера.

    Найстройки:
    level - уровень логгирования сообщений. От указанного и выше.
    rotation - объем файла, при достижении которого создается новый файл логов.
    retention - время, через которое файл логов удаляется.
    compression - сжатие файлов логов для хранения.
    enqueue - использование логгера в асинхронном режиме.
    """

    logger.add(
        'logs/file_{time}.log',
        level='DEBUG',
        rotation="50 MB",
        retention="14 days",
        compression="zip",
        enqueue=True
    )
    return logger
