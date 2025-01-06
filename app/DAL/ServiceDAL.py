"""Методы DAL для управления услугами."""

# THIRDPARTY
from sqlalchemy.ext.asyncio import AsyncSession

# FIRSTPARTY
from app.DAL.BaseDAL import BaseDAL
from app.models.models import ServiceModel


class ServiceDAL(BaseDAL):
    """Методы DAL для управления услугами."""

    model = ServiceModel

    @classmethod
    async def add_one_service(cls, data: ServiceModel, session: AsyncSession):
        """Метод для добавления услуги."""
        new_service = cls.model(
            service_name=data.service_name,
            service_cost=data.service_cost,
            service_time=data.service_time,
        )
        session.add(new_service)
        await session.commit()
        return new_service
