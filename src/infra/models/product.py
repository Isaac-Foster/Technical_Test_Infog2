from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    DateTime,
    event,
    Boolean,
)

from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infra.database.sql import reg


@reg.mapped_as_dataclass
class ProductModel:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    price: Mapped[float] = mapped_column(Numeric(19, 4))
    description: Mapped[str] = mapped_column(String(250), index=True)
    barcode: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    section: Mapped[str] = mapped_column(String(20), index=True)
    stock: Mapped[int] = mapped_column(Integer)
    expiration_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )
    disponibility: Mapped[bool] = mapped_column(Boolean, default=True)
    images: Mapped[List['ImageModel']] = relationship(  # noqa
        'ImageModel',
        back_populates='product',
        cascade='all, delete-orphan',  # Deleta imagens quando produto é deletado
        lazy='select',  # Carrega imagens automaticamente
        init=False,  # Não incluir no __init__
        default_factory=list,  # Lista vazia por padrão
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now, onupdate=datetime.now
    )


@event.listens_for(ProductModel, 'before_insert')
@event.listens_for(ProductModel, 'before_update')
def update_disponibility(mapper, connection, target: ProductModel):
    target.disponibility = target.stock > 0
