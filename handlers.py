from pyrogram import Client, filters
from pyrogram.types import messages_and_media, ReplyKeyboardMarkup, KeyboardButton

from settings import configure_logging


logger = configure_logging()
app = Client("my_account")


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='начать сбор аналитики'
        )
    ]

], one_time_keyboard=True, resize_keyboard=True)

CHAT_ID: int = None


@app.on_message(filters.command('start'))
async def command_start(client: Client, message: messages_and_media.message.Message):
    print('Проверка на авторизацию') # await authorization()
    logger.info('Проверка на авторизацию')
    logger.complete()
    await client.send_message(message.chat.id, 'Вы прошли авторизацию!', reply_markup=reply_keyboard) #
    logger.debug('Вы прошли авторизацию!')


@app.on_message(filters.text == 'начать сбор аналитики')
async def collect_analitycs(client: Client, message: messages_and_media.message.Message):
    print('Бот начал работу')
    await client.send_message(message.chat.id, '...Здесь идет активный сбор данных пользователей...')
    print('...Здесь идет активный сбор данных пользователей...')


app.run()
