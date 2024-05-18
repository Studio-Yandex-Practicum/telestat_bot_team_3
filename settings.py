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
    BOT2_TOKEN = os.environ['BOT2_TOKEN']
    USER_ACCOUNT_NAME = os.environ['USER_ACCOUNT_NAME']
    PHONE_NUMBER = os.environ['PHONE_NUMBER']
    BOT_ACCOUNT_NAME = os.environ['BOT_ACCOUNT_NAME']
    BOT2_ACCOUNT_NAME = os.environ['BOT2_ACCOUNT_NAME']

    # Конфигурация для гугл таблиц
    TYPE = os.environ['TYPE']
    PROJECT_ID = os.environ['PROJECT_ID']
    PRIVATE_KEY_ID = os.environ['PRIVATE_KEY_ID']
    PRIVATE_KEY = '-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDp8UgYk7fN96wR\nV5WcK0tKitnHSk0McpYHYprD0E9Lfu4QWGge/XWpHsLail/l0up5WqvlUHWKYiYR\nes2r3QM0zQi1kjDDtH1lO0fdmtT5gMpGgHseCbGrpzqo9My4O+hSdYEJUsVzfJ7I\nvG6FSj2nVon+66GILxKnAGzbw3e31TpzKOd4+iWR9HNp7NAqHdmb8AGk9rtPwkkX\n69hItPEHtFAJZ5nCAj/kv8sr23OdE8OJyssirA6tF3JlRWMWLhc/54c6LPFyYXGh\nMj+OyaYggmPVLudhx1G5GivF4+P/mJbrXAumbPM3KOrT0h0HKvKrRUDUqNlR1rgu\nZa4E5z8lAgMBAAECggEAMnzl1hYFMECQJEL+cRB/5IPAWcv9gl71ZX0gkPtzLYQk\nfScTO4LwYnIW0+LSrO8ettd8axY488dYV2PlIL7nOv038LWu7AGXIWKQkTEh3wHu\nRZZjW7l0XGsQFBgW2XjmW+trkHdKUTD3NLPD92StFyDsUbWJLDKaiCulkq0l+Gh0\nwthGuWEigHI8saAtYTZwq9aKT+fiPp5pYNmQR/I1TF0JcbD3IGvb94vEj2LauMAZ\nO7YQy59eHguun1Iwge/6KSVmaFzScgXtlHNIFA3/wxGBBLkQC5wVozXTN5FS0q8N\nM9xpAP37OQ9ByLDLotW+2n5f6x0xzBZ4nV0yK4FBOQKBgQD/+qkWdfIVs1YgdZ3G\nLwFa+vvrUyrGGEc0C+QqTFsemyjLqGEmzFJjKTINaLWy0e2BykSJd/0DQiwVmCcz\nvyjO4Wu9RDB2ou2d+WHZo9iNItgoy8/OgHsUS9j7kmqtFS8IbsW8vSB/n8hNk2Hu\nuUfLI49gM8BFOE5cyU+Pszr+WQKBgQDp9ilVg30iU1Jzjf8+4TfazUITqOmP4CHt\nRbcfsYa1sZXcMgfQerCHiKOXJLiLrE5VspiBbd2B1BxCwo9e+yMOIWnbAZawhkbn\n01QiCYLU/1yNr3/oStlv423qFGCPWNLkDQR8Dd17XCVc1vpXHfl+y1dMVidtaSKy\nCGn6oaqlrQKBgQDXP6tRxMpVryD8WIrcbQhhve16m8u7Gg092cX6P4zbtrNeVe+j\n1WpuEeUR23v2q4phenmZczlhtRIm8nP8koE5PdsAI0fxat4O2faLMbjWLXfBDmln\nByj4DzOdkCh99PNAzw0dwZeDWhPwD7/pIwoY6oUU60+BpXBXm7x4ZMl1uQKBgB5u\n++94vDVT21zWssYuK8LVgmvmRAOIJ0GjGPARerF12UWcaHHRE9d9ibImf68DiekR\n406qyO6Tdd2lS1sSlfvHkup/KWfq/5w2XDJVRGSKlzKDCsNfwSsRzYFuhyT+a+ho\nXRX6A76BPQb3m/brGkJJFyEB7/0GeRHpkEee8gC9AoGAaAxsWHOj2g8CQbPnQU1I\noHxG3a8R0PFf0o/60IBTxC7+VcpaRRsEuVinuJVZG8aDWpXLz3D5DMrBvjZU7W6q\nGUAe0CET2X6PKQwXsZgA10yL1iU3ZJu5zlG6QnLvsjpa2GYorrFkkJOqUk3lDyKE\nF9bUJDKwaP8NdcShcdzv+lQ=\n-----END PRIVATE KEY-----'
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
