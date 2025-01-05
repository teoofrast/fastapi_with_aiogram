"""Описание моделей базы данных."""
# STDLIB
from datetime import datetime

# THIRDPARTY
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для БД."""
    pass


# Промежуточная таблица для связи "многие ко многим" между заказами и услугами
order_services = Table(
    'order_services',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id'), primary_key=True)
)


class UserModel(Base):
    """Модель пользователей."""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    # Связь с заказами
    orders: Mapped[list[OrderModel]] = relationship(
        'OrderModel', back_populates='user'
    )


class ServiceModel(Base):
    """Модель услуг."""
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str]
    service_cost: Mapped[int]
    service_time: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Связь с заказами через промежуточную таблицу
    orders: Mapped[list[OrderModel]] = relationship(
        'OrderModel', secondary=order_services, back_populates='services'
    )


class OrderModel(Base):
    """Модель заказов."""
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    begin_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Связь с пользователем
    user: Mapped[UserModel] = relationship(
        'UserModel', back_populates='orders'
    )

    # Связь с услугами через промежуточную таблицу
    services: Mapped[list[ServiceModel]] = relationship(
        'ServiceModel', secondary=order_services, back_populates='orders'
    )
