from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    event,
    select,
    update,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.infra.database.sql import reg
from src.infra.enums.order import OrderStatus
from src.infra.models.order_item import OrderItemModel
from src.infra.models.product import ProductModel
from src.infra.models.user import UserModel


@reg.mapped_as_dataclass
class OrderModel:
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), index=True
    )
    customer_name: Mapped[str] = mapped_column(
        String(255), default='', init=False, index=True
    )
    customer_email: Mapped[str] = mapped_column(
        String(255), default='', init=False, index=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name='status', native_enum=True),
        init=False,
        default=OrderStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relação com os itens do pedido (OrderItemModel)
    items: Mapped[list[OrderItemModel]] = relationship(
        'OrderItemModel',
        backref='order',
        cascade='all, delete-orphan',
        lazy='select',
        init=False,
        default_factory=list,
    )


@event.listens_for(OrderModel, 'before_insert')
def populate_customer_info(mapper, connection, target):
    session = Session(bind=connection)
    user = session.query(UserModel).get(target.customer_id)
    if user:
        target.customer_name = user.name
    else:
        raise ValueError(f'User with ID {target.customer_id} not found.')


@event.listens_for(OrderModel, 'before_update')
def restore_stock_on_cancel(mapper, connection, target: OrderModel):
    if target.status != OrderStatus.CANCELLED:
        return

    stmt = select(OrderItemModel).where(OrderItemModel.order_id == target.id)
    items = connection.execute(stmt).scalars().all()

    for item in items:
        update_stmt = (
            update(ProductModel)
            .where(ProductModel.id == item.product_id)
            .values(stock=ProductModel.stock + item.quantity)
        )
        connection.execute(update_stmt)


@event.listens_for(OrderModel, 'before_delete')
def restore_stock_on_delete(mapper, connection, target: OrderModel):
    stmt = select(UserModel).where(UserModel.order_id == target.id)
    if target.status == OrderStatus.COMPLETED:
        return

    stmt = select(OrderItemModel).where(OrderItemModel.order_id == target.id)
    items = connection.execute(stmt).scalars().all()

    stmt = select(UserModel).where(UserModel.order_id == target.id)

    for item in items:
        update_stmt = (
            update(ProductModel)
            .where(ProductModel.id == item.product_id)
            .values(stock=ProductModel.stock + item.quantity)
        )
        connection.execute(update_stmt)
