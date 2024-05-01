from pyrogram import Client, filters
from pyrogram.types import (messages_and_media, ReplyKeyboardMarkup,
                            KeyboardButton)

from settings import configure_logging


logger = configure_logging()
app = Client("my_account")


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        # Список кнопок для ботов №1 и №2:
        # Для чат-бота №1
        KeyboardButton(
            text='начать сбор аналитики'
        ),
        # Для админки чат-бота №1 и №2
        KeyboardButton(
            text='Добавить администратора'
        ),
        # Для админки чат-бота №1 и №2
        KeyboardButton(
            text='Удалить администратора'
        ),
        # Для админки чат-бота №1
        # Позволяет выбирать телеграм канал из тех, куда загружен бот для
        # отправки запроса.
        KeyboardButton(
            text='Выбрать телеграм канал'
        ),
        # Для админки чат-бота №1
        # Позволяет установить период опроса списка пользователей групп
        # (1 час, 5 часов, 10 часов, 15 часов, 24 часа).
        KeyboardButton(
            text='Установить период сбора данных'
        ),
        # Для админки чат-бота №2
        # Запуск автоматического отчета по заданным критериям
        # Установка периода опроса списка пользователей групп
        # (1 час, 5 часов, 10 часов, 15 часов, 24 часа,
        # ручной ввод даты и времени).
        # Сбор данных осуществляется из гугл таблиц куда собирает
        # информацию бот №1.
        KeyboardButton(
            text='Автоматическое формирование отчёта'
        ),
        # Для админки чат-бота №2
        # Позволяет сформировать отчёт на текущий момент
        # (формирование осуществляется по критериям,
        # заданным при выборе пользователя).
        KeyboardButton(
            text='Формирование отчёта'
        ),
        # Для админки чат-бота №2
        # Позволяет сформировать график на основании сформированного отчёта.
        KeyboardButton(
            text='Формирование графика'
        ),
    ]


], one_time_keyboard=True, resize_keyboard=True)


@app.on_message(filters.command('start'))
async def command_start(client: Client, message:
                        messages_and_media.message.Message):
    # await authorization()
    logger.info('Проверка на авторизацию')
    await client.send_message(message.chat.id, 'Вы прошли авторизацию!',
                              reply_markup=reply_keyboard)
    logger.debug('Вы прошли авторизацию!')


@app.on_message(filters.text == 'начать сбор аналитики')
async def collect_analitycs(client: Client,
                            message: messages_and_media.message.Message):
    logger.info('Бот начал работу')
    await client.send_message(message.chat.id,
                              '.Здесь идет активный сборданных пользователей.')
    logger.info('...Здесь идет активный сбор данных пользователей...')


app.run()
