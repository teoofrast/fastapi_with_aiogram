"""Классы доступа к базовым CRUD операциям."""

# THIRDPARTY
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.models.models import UserModel


class BaseDAL(object):
    """Базовый класс доступа к операциям CRUD."""
    model = None

    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession):
        """Найти запись в БД по ID."""
        sql_query = select(cls.model).filter_by(id=id)
        user = await session.execute(sql_query)
        return user.scalars().one_or_none()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        """Найти все записи в БД"""
        sql_query = select(cls.model)
        result = await session.execute(sql_query)
        return result.scalars().all()


class UserDAL(BaseDAL):
    model = UserModel

    @classmethod
    async def add_one_user(cls, data, session: AsyncSession):
        new_user = cls.model(
            id = data.id,
            username = data.username,
            first_name = data.first_name,
            last_name = data.last_name,
        )
        session.add(new_user)
        await session.commit()
        return new_user
