from datetime import datetime as dt

from sqlalchemy import (BigInteger, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Integer, String)

from core.db import Base


class ChannelSettings(Base):
    """Модель настроек пользователя для каналов."""

    usertg_id = Column(
        BigInteger,
        ForeignKey(
            'userstg.user_id',
            ondelete='CASCADE'))
    channel_name = Column(String(100), nullable=False)
    period = Column(Integer, default=3600)
    work_period = Column(DateTime, nullable=False)
    remaining_work_time = Column(DateTime)
    created = Column(DateTime, default=dt.now)
    refreshed = Column(DateTime, default=dt.now, onupdate=dt.now)
    # previously_refresh = Column(
    #     DateTime,
    #     default=dt.now() - (dt.now() - datetime.datetime.timedelta(seconds=refreshed)))
    started_at = Column(DateTime, nullable=False)
    # stoped_by = Column(DateTime, default=dt.now() + datetime.datetime.timedelta(seconds=work_period))
    run_status = Column(Boolean, default=False)
    run = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return (f'{self.usertg_id}'
                f'{self.channel_name},'
                f'{self.period},'
                f'{self.work_period},'
                f'{self.remaining_work_time},'
                f'{self.created}'
                f'{self.refreshed},'
                # f'{self.previously_refresh},'
                f'{self.started_at},'
                # f'{self.stoped_by},'
                f'{self.run_status},'
                f'{self.run}')
