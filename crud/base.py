from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс операций CRUD."""

    def __init__(
            self,
            model):
        self.model = model

    async def get_by_attr(
            self,
            attr_name,
            attr_value,
            session: AsyncSession,
    ):
        """Получение значения из ДБ по атрибуту."""

        attr = getattr(self.model, attr_name)
        return ((await session.execute(
            select(self.model).where(
                attr == attr_value))).first())

    async def create(
            self,
            obj,
            session: AsyncSession,
    ):
        """Обновление значений в таблице ДБ."""

        db_obj = self.model(**obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
