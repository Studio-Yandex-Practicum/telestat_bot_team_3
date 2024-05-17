from crud.channel_settings import channel_settings_crud
from core.db import engine


async def get_channels():
    async with engine.connect() as session:
        channel_btns = []
        for channel in await channel_settings_crud.get_all(session):
            channel_btns.append(channel.channel_name)
        return channel_btns


async def get_run_status(channel):
    async with engine.connect() as session:
        obj_channel = await channel_settings_crud.get_by_attr(
            attr_name='channel_name',
            attr_value=channel,
            session=session
        )
        print('ПРИНТУЕМ СТАТУСЫ')
        return obj_channel.run


async def set_channel_stop_attr(channel):
    async with engine.connect() as session:
        obj = {
            'run_status': False,
            'run': False
        }
        channels = await channel_settings_crud.set_update(
            attr_name='channel_name',
            attr_value=channel,
            obj_in=obj,
            session=session
        )
        return channels
