from datetime import datetime as dt

from sqlalchemy import Column, DateTime, String

from core.db import Base


class Report(Base):
    """Модель для хранения ссылок сформированных отчётов."""

    link = Column(String(512), unique=True, index=True)
    create = Column(DateTime, default=dt.now)
    group = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return (
            f'{self.id},'
            f'{self.link},'
            f'{self.create},'
            f'{self.group}'
        )
