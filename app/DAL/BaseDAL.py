"""Классы доступа к базовым CRUD операциям."""

# STDLIB
from typing import List, Optional, Type

# THIRDPARTY
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.models import UserModel


class BaseDAL(object):
    """Базовый класс доступа к операциям CRUD."""

    model = None

    @classmethod
    async def get_by_id(
        cls: Type['BaseDAL'], id_: int, session: AsyncSession
    ) -> Optional[Type['model']]:
        """Найти запись в БД по ID."""
        sql_query = select(cls.model).filter_by(id=id_)
        user = await session.execute(sql_query)
        return user.scalars().one_or_none()

    @classmethod
    async def get_all(
        cls: Type['BaseDAL'], session: AsyncSession
    ) -> List[Type['model']]:
        """Найти все записи в БД."""
        sql_query = select(cls.model)
        result = await session.execute(sql_query)
        return result.scalars().all()


class UserDAL(BaseDAL):
    """Класс для управление юзерами."""

    model = UserModel

    @classmethod
    async def add_one_user(
        cls: Type['UserDAL'], data: UserModel, session: AsyncSession
    ) -> UserModel:
        """Метод для добавления нового юзера."""
        new_user = cls.model(
            id=data.id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        session.add(new_user)
        await session.commit()
        return new_user
