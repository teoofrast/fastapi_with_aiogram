"""Определение pydantic-схем."""

# THIRDPARTY
from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    """Схема для валидации данных пользователя."""

    id: int = Field(ge=0)
    username: str | None
    first_name: str | None
    last_name: str | None


class ServiceCreateSchema(BaseModel):
    """Схема для валидации данных услуг."""

    service_name: str
    service_cost: int
    service_time: int
