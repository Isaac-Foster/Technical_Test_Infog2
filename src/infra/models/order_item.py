from sqlalchemy import event
from sqlalchemy.orm import Session

@reg.mapped_as_dataclass
class OrderItemModel:
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)

    product: Mapped[ProductModel] = relationship(
        init=False,
        lazy='joined'
    )

# Listener que será chamado antes de inserir um novo item de pedido
@event.listens_for(OrderItemModel, 'before_insert')
def check_and_decrement_stock(mapper, connection, target: OrderItemModel):
    session = Session(bind=connection)
    
    # Busca o produto com bloqueio de linha (FOR UPDATE) para evitar race conditions
    product = session.get(ProductModel, target.product_id, with_for_update=True)

    if not product:
        raise ValueError("Product does not exist")

    if product.stock < target.quantity:
        raise ValueError(
            f"Not enough stock for product {product.name}. Available: {product.stock}, Requested: {target.quantity}"
        )

    # Atualiza o estoque
    product.stock -= target.quantity

    session.add(product)
    session.flush()
