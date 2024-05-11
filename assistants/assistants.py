from functools import wraps

from pyrogram import Client
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup

from crud.userstg import userstg_crud
from settings import Config, logger

user_bot = Client(
    Config.ACCOUNT_NAME,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    phone_number=Config.PHONE_NUMBER
)


class DotNotationDict(dict):
    """
    Класс добавления магических атрибутов к словарю.
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


async def check_by_attr(attr_name, attr_value, session) -> bool:
    """Проверка id на наличие в ДБ."""

    if await userstg_crud.get_by_attr(
            attr_name,
            attr_value,
            session
            ) is None:
        return False
    return True


def dinamic_ceyboard(objs, attr_name, ceyboard_row=2):
    """
    Динамическая клавиатура для вывода в телеграм.
    objs - итерируемый объект или объекты,
    attr_name - атрибут который из текущего объекта будет
        отображаться в виде названия кнопки,
    ceyboard_row - пределитель колличества кнопок на одну строку.
    """
    logger.info('Процесс построения динамической клавиатуры запущен!')
    btn_row = []
    btn_many = []
    counter = ceyboard_row
    for obj in objs:
        counter -= 1
        btn_row.append(KeyboardButton(
            text=getattr(obj, attr_name))
            )
        if counter == 0:
            counter = ceyboard_row
            btn_many.append(btn_row)
            btn_row = []

    if not btn_many:
        ceyboard = ReplyKeyboardMarkup(keyboard=[
            btn_row
        ], resize_keyboard=True)
    else:
        print(btn_many)
        ceyboard = ReplyKeyboardMarkup(
            keyboard=btn_many,
            resize_keyboard=True)
    logger.info('Динамическая клавиатура сформирована успешно.')
    return ceyboard


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
