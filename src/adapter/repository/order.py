from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload

from src.infra.models.order import OrderModel
from src.infra.models.order_item import OrderItemModel
from src.interfaces.schema.order import OrderCreateSchema

from src.adapter.repository.public import BaseRepo
from src.interfaces.schema.order import OrderSchema
from src.adapter.repository.product import ProductRepo


class OrderRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.product = ProductRepo()
        self.model = OrderModel
        self.item_model = OrderItemModel
        self.public = OrderSchema

    def create(self, data: OrderCreateSchema, user):
        model = self.model(
            customer_id=user.id,
        )
        order_data = None

        with self.session() as session:
            session.add(model)
            session.flush()

            for item in data.items:
                item_model = self.item_model(
                    order_id=model.id,
                    product_id=item.id,
                    quantity=item.quantity,
                )
                session.add(item_model)
                session.flush()

            session.flush()
            session.refresh(model)

            # Força o carregamento dos items antes de encerrar a sessão
            _ = (
                model.items
            )  # ou: session.refresh(model, ["items"]) se for necessário

            # Cria uma cópia "desanexada" com todos os dados necessários
            order_data = self.public.model_validate(
                model, from_attributes=True
            )
            session.commit()
        return order_data

    def find_all(self, **kwargs):
        section = kwargs.get('section')
        status = kwargs.get('status')
        order_id = kwargs.get('id')
        customer_id = kwargs.get('customer_id')
        start_date = kwargs.get('start')
        end_date = kwargs.get('end')

        stmt = (
            select(OrderModel)
            .join(OrderModel.items)
            .join(OrderItemModel.product)
            .options(
                selectinload(OrderModel.items).selectinload(
                    OrderItemModel.product
                )
            )
            .distinct()
        )

        filters = []

        if status:
            filters.append(OrderModel.status == status)

        if order_id:
            filters.append(OrderModel.id == order_id)

        if customer_id:
            filters.append(OrderModel.customer_id == customer_id)

        if start_date and end_date:
            filters.append(OrderModel.created_at.between(start_date, end_date))
        elif start_date:
            filters.append(OrderModel.created_at >= start_date)
        elif end_date:
            filters.append(OrderModel.created_at <= end_date)

        if section:
            stmt = stmt.join(OrderModel.items)
            filters.append(OrderItemModel.section == section)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.order_by(OrderModel.created_at.desc())

        with self.session() as session:
            result = session.execute(stmt).scalars().unique().all()
            return [
                self.public.model_validate(order, from_attributes=True)
                for order in result
            ]

    def delete(self, **kwargs):
        already = self.find(**kwargs)

        if not already:
            raise Exception('order not found')

        with self.session() as session:
            try:
                # Busca o pedido com os itens
                order = (
                    session.query(self.model)
                    .options(selectinload(self.model.items))
                    .filter_by(**kwargs)
                    .first()
                )

                #print(order)

                if not order:
                    raise Exception('order not found in DB')

                # Deleta itens um por um para ativar o listener
                for item in order.items:
                    ##print(item)
                    session.delete(item)
                    session.flush()

                # Deleta o pedido
                session.execute(delete(self.model).filter_by(id=order.id))
                session.commit()

                return already  # retorna os dados validados do pedido já coletados
            except Exception as e:
                print(e)
                return False
