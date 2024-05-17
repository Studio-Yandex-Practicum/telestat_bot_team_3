from enum import Enum
import re
import datetime
from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import (UsernameNotOccupied,
                                                        UserNotParticipant)
from pyrogram.types import ReplyKeyboardRemove, messages_and_media

from assistants.assistants import dinamic_keyboard
from buttons import bot_keys
from logic import (choise_channel, add_admin, del_admin,
                   set_settings_for_analitics)
from services.telegram_service import ChatUserInfo, get_settings_from_report
from services.google_api_service import get_report
from permissions.permissions import check_authorization
from settings import Config, configure_logging


logger = configure_logging()


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    choise_channel = 'Выбрать телеграм канал'
    set_period = 'Установить период сбора данных'
    run_collect_analitics = 'Начать сбор аналитики'
    user_period = 'Свой вариант'


class BotManager:
    add_admin_flag = False
    del_admin_flag = False
    choise_channel_flag = False
    set_period_flag = False
    owner_or_admin = ''
    chanel = ''
    period = 10
    work_period = 60


bot_1 = Client(
    Config.BOT_ACCOUNT_NAME,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT_TOKEN
)

manager = BotManager()


@bot_1.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка на авторизацию')

    if await check_authorization(message.from_user.id, is_superuser=True):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как владелец!',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[:3],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'owner'
        logger.debug(f'{message.chat.username} авторизован как владелец!')
    elif await check_authorization(message.from_user.id):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как администратор бота!',
            reply_markup=dinamic_keyboard(
                objs=[bot_keys[2]],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'admin'
        logger.debug(f'{message.chat.username} авторизован как администратор бота!')


@bot_1.on_message(filters.regex(Commands.add_admin.value))
async def command_add_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Добавление администратора в ДБ."""

    if manager.owner_or_admin == 'owner':
        logger.info('Добавляем администратора')

        await client.send_message(
            message.chat.id,
            'Укажите никнеймы пользователей, которых хотите добавить '
            'в качестве администраторов, в формате:'
            'nickname1, nickname2, nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.add_admin_flag = True


@bot_1.on_message(filters.regex(Commands.del_admin.value))
async def command_del_admin(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Блокирует администраторов бота в ДБ."""

    if manager.owner_or_admin == 'owner':
        logger.info('Блокируем администратора(ов) бота')
        await client.send_message(
            message.chat.id,
            'Укажите никнеймы администраторов, которых хотите деактивировать, '
            'в формате nickname1, nickname2, nickname3',
            reply_markup=ReplyKeyboardRemove()
        )
        manager.del_admin_flag = True


@bot_1.on_message(filters.regex(Commands.run_collect_analitics.value))
async def generate_report(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Отправляет отчёт."""

    try:
        if not manager.chanel:
            print('CHANNEL THIS:', manager.chanel)
            raise TypeError

        settings = {
            'usertg_id': (await client.get_users(message.from_user.username)).id,
            'channel_name': manager.chanel,
            'period': manager.period,
            'work_period': datetime.datetime.now() + datetime.timedelta(seconds=manager.work_period),
            'started_at': datetime.datetime.now(),
            'run_status': True,
            'run': True
        }

        await set_settings_for_analitics(client, message, settings)
        period = manager.period
        usertg_id = (await client.get_users(message.from_user.username)).id
        channel_name = manager.chanel

        async def recursion_func(usertg_id, channel_name, period):

            # chat = ChatUserInfo(bot_1, 'telestat_team')
            # logger.info('Бот начал работу')
            # report = await chat.create_report()
            # reports_url = await get_report(report)
            # for msg in reports_url:
            #     await client.send_message(
            #         message.chat.id,
            #         msg
            #     )

            print(datetime.datetime.now())
            await sleep(period)
            db = await get_settings_from_report(
                    {
                        'usertg_id': usertg_id,
                        'channel_name': channel_name
                    })

            if (not db.run or db.work_period <= datetime.datetime.now()):
                logger.info('Удалили запись в базе данных вышли из рекурсии.')
                return
            await recursion_func(db.usertg_id, db.channel_name, db.period)

        await recursion_func(usertg_id, channel_name, period)

    # except TypeError:
    #     logger.info('Запуск процесса сбора аналитики невозможен. '
    #                 'Выбирите канал и попробуте снова!')
    except KeyboardInterrupt:
        pass


@bot_1.on_message(filters.regex(Commands.choise_channel.value))
async def choise_channel_cmd(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Находит все каналы владельца."""

    logger.info('Выбираем телеграм канал')
    await client.send_message(
            message.chat.id,
            'Идёт процесс получения каналов, пожалуйста, подождите...',
            reply_markup=ReplyKeyboardRemove()
        )
    if manager.owner_or_admin == 'owner' or manager.owner_or_admin == 'admin':
        await choise_channel(client, message)
        manager.choise_channel_flag = True


@bot_1.on_message(filters.regex(Commands.set_period.value))
async def set_period_cmd(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Устанавливает переиод сбора данных."""

    logger.info('Устананавливаем период сбора данных')
    if manager.owner_or_admin == 'owner' or manager.owner_or_admin == 'admin':
        await client.send_message(
            message.chat.id,
            'Установите период опроса списка пользователей группы:',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[8:14],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.set_period_flag = True


@bot_1.on_message(filters.regex(Commands.user_period.value))
async def set_user_period(
    client: Client,
    message: messages_and_media.message.Message
):
    """Устанавливает пользовательское время периода опроса."""

    logger.info('Пользователь вручную выбирает время опроса')
    await client.send_message(
        message.chat.id,
        'Укажите произвольное время в часах:',
        reply_markup=ReplyKeyboardRemove()
    )


@bot_1.on_message()
async def all_incomming_messages(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Здесь обрабатываем все входящие сообщения."""

    if manager.add_admin_flag:
        await add_admin(client, message)
        manager.add_admin_flag = False

    elif manager.del_admin_flag:
        await del_admin(client, message)
        manager.del_admin_flag = False

    elif manager.choise_channel_flag:
        try:
            if ((await client.get_chat_member(
                message.text,
                Config.BOT_ACCOUNT_NAME)
                    ).privileges.can_restrict_members):
                manager.chanel = message.text
                await client.send_message(
                    message.chat.id,
                    'Выберете периодичность сбора аналитики.',
                    reply_markup=dinamic_keyboard(
                        objs=bot_keys[3:5],
                        attr_name='key_name',
                        keyboard_row=2
                    )
                )
        except UsernameNotOccupied as e:
            logger.error(f'Название канала введено не корректно или не занято!\n {e}')
            await client.send_message(
                    message.chat.id,
                    'Вероятно В ведённом канале "Бот" не зарегистрирован!',
                    reply_markup=dinamic_keyboard(
                        objs=[bot_keys[2]],
                        attr_name='key_name'
                    )
                )
        except UserNotParticipant as e:
            logger.error(f'В ведённом канале "Бот" не зарегистрирован!\n {e}')
            await client.send_message(
                message.chat.id,
                'Вероятно В ведённом канале "Бот" не зарегистрирован!',
                reply_markup=dinamic_keyboard(
                    objs=([bot_keys[2]],
                          bot_keys[:3])[manager.owner_or_admin == 'owner'],
                    attr_name='key_name'
                )
            )
        manager.choise_channel_flag = False

    elif manager.set_period_flag:
        logger.info('Проверка и сохранение периода опроса в manager')
        period = re.search('\d{,3}', message.text).group()
        if not period:
            await client.send_message(
                message.chat.id,
                'Проверьте правильность периода, должно быть целое число!\n'
                'Укажите произвольное время в часах:',
                reply_markup=ReplyKeyboardRemove()
            )
            return
        await client.send_message(
            message.chat.id,
            'Для запуска сбора статистики нажмите кнопку.',
            reply_markup=dinamic_keyboard(
                objs=[bot_keys[4]],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.period = period * 3600
        manager.set_period_flag = False
        logger.info(f'Выбран период опроса {manager.period}')

    else:
        await client.send_message(
            message.chat.id,
            'Упс, этого действия мы от вас не ожидали! \n'
            'Или вы пытаетесь выполнить действие на которое '
            'у вас нет прав, "Авторизуйтесь", командой: /start'
        )
        manager.owner_or_admin = ''


if __name__ == '__main__':
    logger.info(' Бот запущен')
    bot_1.run()
