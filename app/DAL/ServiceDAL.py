from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.DAL.BaseDAL import BaseDAL

from app.models.models import ServiceModel


class ServiceDAL(BaseDAL):
    model = ServiceModel

    @classmethod
    async def add_one_service(cls, data: ServiceModel, session: AsyncSession):
        new_service = cls.model(
            service_name=data.service_name,
            service_cost=data.service_cost,
            service_time=data.service_time,
        )
        session.add(new_service)
        await session.commit()
        return new_service