import os
import glob
import asyncio
import argparse

from pyrogram import Client
from settings import Config, logger

from service.telegram_service import add_users
from crud.userstg import userstg_crud


START_TEXT = """
   _____       _                                            ___           _   
  (_   _)     (_ )                                         (  _`\        ( )_ 
    | |   __   | |    __     __   _ __   _ _   ___ ___     | (_) )   _   | ,_)
    | | /'__`\ | |  /'__`\ /'_ `\( '__)/'_` )/' _ ` _ `\   |  _ <' /'_`\ | |  
    | |(  ___/ | | (  ___/( (_) || |  ( (_| || ( ) ( ) |   | (_) )( (_) )| |_ 
    (_)`\____)(___)`\____)`\__  |(_)  `\__,_)(_) (_) (_)   (____/'`\___/'`\__)
                          ( )_) |                                             
                           \___/'                                             

Выберите действие:

    1. Первичный запуск (инициализация/настройка)
    2. Запуск ботов
"""


def register_sessions():
    """
    Функция создания сессии подключения к telegram.

    Возвращает username созданной сессии.
    """

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID или API_HASH не найдены в файле .env")

    session_name = input('\nВведите имя сессии (нажмите Enter после ввода): ')

    if not session_name:
        return None

    session = Client(
        name=session_name,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workdir="sessions/"
    )

    # async with session:
    user_data = session.get_me()

    logger.success(
        f'Сессия успешно добавлена @{user_data.username} | '
        f'{user_data.first_name} {user_data.last_name}')

    return user_data.username


def get_username_from_session_name(session_name):
    """
    Функция получения username из сохраненной сессии.
    Принимает обязательным аргументом имя сессии session_name.
    """

    session = Client(session_name)

    # async with session:
    user_data = session.get_me()
    return user_data.username


def get_session_name():
    """Функция проверяет наличие файла сессии, возвращает имя сессии."""
    # session_names = glob.glob('sessions/*.session')
    # session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]

    file = glob.glob('*.session')

    if not file:
        session_name = None
        # print('запускаем создание сессии')
        # session_name = register_sessions()
    else:
        session_name = os.path.splitext(os.path.basename(file[0]))[0]
        print(f'Сессия уже создана: {session_name}')
    return session_name


def get_superuser():
    """
    Функция получения суперюзера из базы данных.

    Возвращает username суперюзера.
    Если суперюзера в базе нет, то возвращает None.
    """

    print('Возвращаем суперюзера из бд')
    superuser = userstg_crud.get_by_attr(is_superuser=True)
    return superuser


def create_superuser(username=None):
    """
    Функция создания суперюзера.

    Функция ждет ввода username телеграмма для регистрации его в качестве
    суперюзера.
    """

    print('Создаем суперюзера')
    if not username:
        username = input('Введите username телеграм без символа @')
        if username.startswith('@'):
            username.strip('@')
    add_users(username, is_superuser=True, is_active=True)


def process() -> None:
    """Функция назначения и проверки аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Бот для сбора аналитики')
    parser.add_argument(
        '-i', '--init',
        action='store_true',
        help='initial launch'
    )

    print(get_session_name())

    args = parser.parse_args()


    # if args.init:
    run_initialization() if args.init else print('Обычный запуск')
    # elif action == 2:
    #     tg_clients = await get_tg_clients()

    #     await run_tasks(tg_clients=tg_clients)


def run_initialization():
    """
    Основная логика процесса инициализации.

    Проверяется наличие файла сессии в проекте.
    Проверяется наличие суперпользователя в базе данных.
    При необходимости запускается процесс создания сессии подключения телеграм
    и добавление пользователя в качестве суперпользователя.
    """
    # check_db_connect()
    session_name = get_session_name()
    username = get_username_from_session_name(session_name)
    print('run_initialization, сессия:', session_name)
    superuser = get_superuser()
    if not superuser:
        create_superuser(username)


# run_initialization()

process()
