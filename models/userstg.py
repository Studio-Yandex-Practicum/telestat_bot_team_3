from datetime import datetime as dt

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer, String

from core.db import Base


class UsersTG(Base):
    """Модель пользователя ТГ."""

    user_id = Column(String(100), unique=True)  # Не занаю как будет id=@1234567890 поэтому стринг
    user_name = Column(String(100))
    create_date = Column(DateTime, default=dt.now)
    is_superuser = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f'{self.user_name}'
