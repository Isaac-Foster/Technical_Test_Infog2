from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.infra.database.sql import reg
from src.infra.models.order_item import OrderItemModel

@reg.mapped_as_dataclass
class OrderModel:
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(50), default='pending')
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relação com os itens do pedido (OrderItemModel)
    items: Mapped[list[OrderItemModel]] = relationship(
        'OrderItemModel',
        backref='order',
        cascade='all, delete-orphan',
        lazy='joined'
    )
