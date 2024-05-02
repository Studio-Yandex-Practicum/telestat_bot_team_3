from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from settings import Config


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

print(Config.DB_URI)
engine = create_async_engine(
    Config.DB_URI,
    echo=True)

async_session = AsyncSession(engine)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Получение асинхронных сессий."""

    async with AsyncSessionLocal() as async_session:
        yield async_session
