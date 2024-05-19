from enum import Enum
import re
from pyrogram import Client, filters
from pyrogram.types import messages_and_media, ReplyKeyboardRemove

from settings import configure_logging
from buttons import bot_keys
from logic import (
    add_admin, choise_channel, del_admin, auto_generate_report, generate_report, scheduling
)
from permissions.permissions import check_authorization
from assistants.assistants import dinamic_keyboard
from settings import Config
from services.google_api_service import get_report


class Commands(Enum):
    add_admin = 'Добавить администратора'
    del_admin = 'Удалить администратора'
    auto_report = 'Автоматическое формирование отчёта'
    generate_report = 'Формирование отчёта'
    scheduling = 'Формирование графика'


logger = configure_logging()
bot_2 = Client(
    Config.BOT2_ACCOUNT_NAME,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    bot_token=Config.BOT2_TOKEN
)


class BotManager:
    """Конфигурация глобальных настроек бота."""
    add_admin_flag = False
    del_admin_flag = False
    choise_data_flag = False
    set_period_flag = False
    stop_channel_flag = True
    owner_or_admin = ''
    chanel = ''
    period = 10
    work_period = 60


manager = BotManager()


@bot_2.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Обработчик команды на запуск бота по сбору данных."""

    logger.info('Проверка авторизации.')

    if await check_authorization(message.from_user.id, is_superuser=True):
        await client.send_message(
            message.chat.id,
            f'{message.chat.username} вы авторизованы как владелец!',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[:3] + bot_keys[14:15],
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
                objs=bot_keys[2:3] + bot_keys[14:15],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.owner_or_admin = 'admin'
        logger.debug(
            f'{message.chat.username} авторизован как администратор бота!'
            )







@bot_2.on_message(filters.regex(Commands.add_admin.value))
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


@bot_2.on_message(filters.regex(Commands.del_admin.value))
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






@bot_2.on_message(filters.regex(Commands.auto_report.value))
async def auto_report(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Отправляет отчёт."""

    try:
        if not manager.chanel:
            return

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
    except IntegrityError:
        logger.info(
            'Процесс сбора аналитики в этом канале уже запущен!\n'
            f'Обновляем период сбора аналитики в канале {manager.chanel} '
            f'на {manager.period}'
        )

        await set_channel_data(manager.chanel, manager.period)

    period = manager.period
    usertg_id = (await client.get_users(message.from_user.username)).id
    channel_name = manager.chanel

    await client.send_message(
        message.chat.id,
        f'Бот выполняет сбор аналитики на канале: {channel_name} '
        f'с заданым периодом {period}. Желаете запустить другой '
        'канал? Выполните команду старт: /start',
        reply_markup=ReplyKeyboardRemove()
    )

    async def recursion_func(usertg_id, channel_name, period):
        logger.info('Рекурсия началась')

        # await generate_report()

        logger.info(f'Рекурсия, контрольная точка: {datetime.datetime.now()}')
        db = await get_settings_from_report(
                {
                    'usertg_id': usertg_id,
                    'channel_name': channel_name
                })
        if db is not None or db:
            # await custom_sleep(channel_name, period)
            await sleep(period)
            if (not db.run or db.work_period <= datetime.datetime.now()):
                logger.info(f'Удаляем запись о канале: {db.channel_name} '
                            'в базе данных, Бот закончил свою работу.')
                await delete_settings_report('id', db.id)
                return
            await recursion_func(db.usertg_id, db.channel_name, db.period)

    await recursion_func(usertg_id, channel_name, period)


# @bot_2.on_message(filters.regex(Commands.choise_channel.value))
# async def choise_channel_cmd(
#     client: Client,
#     message: messages_and_media.message.Message,
#     manager=manager
# ):
#     """Находит все каналы владельца."""

#     logger.info('Выбираем телеграм канал')
#     await client.send_message(
#             message.chat.id,
#             'Идёт процесс получения каналов, пожалуйста, подождите...',
#             reply_markup=ReplyKeyboardRemove()
#         )
#     if manager.owner_or_admin == 'owner' or manager.owner_or_admin == 'admin':
#         await choise_channel(client, message)
#         manager.choise_channel_flag = True


@bot_2.on_message(filters.regex(Commands.generate_report.value))
async def generate_report(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Формирует отчет из гугл таблиц."""

    logger.info('Выбираем данные для отчета')

    if manager.owner_or_admin == 'owner' or manager.owner_or_admin == 'admin':
        await choise_channel()
        manager.choise_channel_flag = True


# @bot_2.on_message(filters.regex(Commands.set_period.value))
async def set_period_cmd(
    client: Client,
    message: messages_and_media.message.Message,
    manager=manager
):
    """Устанавливает период формирования отчета."""

    logger.info('Устананавливаем период формирования отчета')
    if manager.owner_or_admin == 'owner' or manager.owner_or_admin == 'admin':
        await client.send_message(
            message.chat.id,
            'Установите период формирования отчета по каналу:',
            reply_markup=dinamic_keyboard(
                objs=bot_keys[8:14],
                attr_name='key_name',
                keyboard_row=2
            )
        )
        manager.set_period_flag = True


@bot_2.on_message(filters.regex(Commands.user_period.value))
async def set_user_period(
    client: Client,
    message: messages_and_media.message.Message
):
    """Устанавливает пользовательское время периода формирования отчета."""

    logger.info('Пользователь вручную выбирает период формирования отчета')
    await client.send_message(
        message.chat.id,
        'Укажите произвольное время в часах:',
        reply_markup=ReplyKeyboardRemove()
    )


# @bot_2.on_message(filters.regex(Commands.stop_report.value))
# async def stop_report(
#     client: Client,
#     message: messages_and_media.message.Message,
#     manager=manager
# ):
#     """Функция для остановки запущенных процессов формирования отчетов."""
#     logger.info('Запущена процесс остановки формирования отчетов.')
#     channel_btns = []
#     channels = get_channels_from_db()

#     if not channels:
#         await client.send_message(
#             message.chat.id,
#             'Нет запущеных задач по сбору аналитики!',
#             reply_markup=dinamic_keyboard(
#                 objs=(
#                     [bot_keys[2:3] + bot_keys[14:15]],
#                     bot_keys[:3] + bot_keys[14:15]
#                 )[manager.owner_or_admin == 'owner'],
#                 attr_name='key_name'
#             )
#         )
#     for channel in await channels:
#         channel_btns.append(DotNotationDict({'channel': channel}))
#     await client.send_message(
#         message.chat.id,
#         'Выберите канал для остановки формирования отчетов:',
#         reply_markup=dinamic_keyboard(
#             objs=channel_btns,
#             attr_name='channel'
#         )
#     )
#     manager.stop_report_flag = True


@bot_2.on_message()
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
        # выбираем канал, по которому хотим получить отчет
        # Собираем данные с канала
        # Формируем словарь data
        data = {}  # формат словаря?
        report_url = await get_report(data)  # получаем данные с гугл таблиц
        await client.send_message(
            message.chat.id,
            report_url
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
        manager.period = int(period) * 3600
        manager.set_period_flag = False
        logger.info(f'Выбран период опроса {manager.period}')

    # elif manager.stop_report_flag:
    #     channel = message.text
    #     await set_channel_data(channel)
    #     logger.info(f'Формирование отчетов с канала {channel} остановлено')
    #     await delete_settings_report('channel_name', channel)
    #     await client.send_message(
    #         message.chat.id,
    #         f'Формирование отчетов с канала {channel} остановлено',
    #         reply_markup=dinamic_keyboard(
    #             objs=(
    #                 [bot_keys[2:3] + bot_keys[14:15]],
    #                 bot_keys[:3] + bot_keys[14:15]
    #             )[manager.owner_or_admin == 'owner'],
    #             attr_name='key_name'
    #         )
    #     )
    #     manager.stop_channel_flag = True
    else:
        await client.send_message(
            message.chat.id,
            'Упс, этого действия мы от вас не ожидали! \n'
            'Или вы пытаетесь выполнить действие на которое '
            'у вас нет прав, "Авторизуйтесь", командой: /start'
        )
        manager.owner_or_admin = ''





if __name__ == '__main__':
    logger.info('Bot 2 is started.')
    bot_2.run()
