"""Управление доступа к БД."""
# STDLIB
from typing import Annotated

# THIRDPARTY
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

database_url = 'sqlite+aiosqlite:///db.sqlite3'
engine = create_async_engine(url=database_url)
new_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Создает и возвращает асинхронную сессию базы данных.

    Эта функция обрабатывает создание новой асинхронной сессии базы данных
    и передает ее с использованием `yield`. Сессия используется для
    выполнения операций с базой данных и автоматически закрывается после
    завершения работы с ней.

    Возвращаемое значение:
        AsyncSession: Асинхронная сессия базы данных.
    """
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
