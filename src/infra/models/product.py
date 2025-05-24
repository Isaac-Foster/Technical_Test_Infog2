from decimal import Decimal
from typing import List, Optional
from datetime import datetime


from sqlalchemy import (
    String,
    Integer,
    Numeric,
    ARRAY,
    DateTime,
    event,
    Boolean,
)

from sqlalchemy.orm import mapped_column, Mapped
from src.infra.database.sql import reg


@reg.mapped_as_dataclass
class ProductModel:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(19, 4))
    description: Mapped[str] = mapped_column(String(512), index=True)
    barcode: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    section: Mapped[str] = mapped_column(String(50), index=True)
    stock: Mapped[int] = mapped_column(Integer)
    expiration_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    disponibility: Mapped[bool] = mapped_column(Boolean, default=True)
    images: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )


@event.listens_for(ProductModel, 'before_insert')
@event.listens_for(ProductModel, 'before_update')
def update_disponibility(mapper, connection, target: ProductModel):
    target.disponibility = target.stock > 0
