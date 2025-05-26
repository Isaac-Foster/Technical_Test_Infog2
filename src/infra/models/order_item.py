from sqlalchemy import event, Integer, ForeignKey, Numeric, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.infra.database.sql import reg
from src.infra.models.product import ProductModel


@reg.mapped_as_dataclass
class OrderItemModel:
    __tablename__ = 'order_items'
    __mapper_args__ = {"confirm_deleted_rows": False}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, init=False, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    price_unit: Mapped[float] = mapped_column(Numeric(19, 4), init=False)
    section: Mapped[str] = mapped_column(init=False)
    total: Mapped[float] = mapped_column(Numeric(19, 4), init=False)
    quantity: Mapped[int] = mapped_column(Integer)

    product: Mapped[ProductModel] = relationship(init=False, lazy='joined')


# Listener que será chamado antes de inserir um novo item de pedido
@event.listens_for(OrderItemModel, 'before_insert')
def check_and_decrement_stock(mapper, connection, target: OrderItemModel):
    product_table = ProductModel.__table__

    # Busca preço e estoque do produto com FOR UPDATE para bloqueio
    stmt = (
        select(
            product_table.c.price,
            product_table.c.stock,
            product_table.c.section,
        )
        .where(product_table.c.id == target.product_id)
        .with_for_update()
    )
    result = connection.execute(stmt).first()

    if result is None:
        raise ValueError('Product does not exist')

    price, stock, section = result

    if stock < target.quantity:
        raise ValueError(
            f'Not enough stock for product {target.product_id}. Available: {stock}, Requested: {target.quantity}'
        )

    # Atualiza estoque no banco
    update_stmt = (
        update(product_table)
        .where(product_table.c.id == target.product_id)
        .values(stock=stock - target.quantity)
    )
    connection.execute(update_stmt)

    # Define preço unitário e total no item do pedido
    target.section = section
    target.price_unit = float(price)
    target.total = target.price_unit * target.quantity


@event.listens_for(OrderItemModel, 'before_delete')
def restore_stock_on_delete(mapper, connection, target: OrderItemModel):
    product_table = ProductModel.__table__
    order_table = reg.metadata.tables['orders']

    # Busca o pedido para verificar status
    order_stmt = select(order_table.c.status).where(
        order_table.c.id == target.order_id
    )
    order_result = connection.execute(order_stmt).first()

    if order_result is None:
        raise ValueError('Order not found')

    order_status = order_result[0]

    if order_status != 'completed':
        # Busca estoque atual do produto
        product_stmt = select(product_table.c.stock).where(
            product_table.c.id == target.product_id
        )
        product_result = connection.execute(product_stmt).first()

        if product_result is None:
            raise ValueError('Product not found')

        current_stock = product_result[0]

        # Atualiza estoque somando a quantidade do item deletado
        update_stmt = (
            update(product_table)
            .where(product_table.c.id == target.product_id)
            .values(stock=current_stock + target.quantity)
        )
        connection.execute(update_stmt)
