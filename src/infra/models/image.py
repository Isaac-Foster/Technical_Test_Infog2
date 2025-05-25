from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, Integer, String, DateTime, event

from src.infra.database.sql import reg


@reg.mapped_as_dataclass
class ImageModel:
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('products.id', ondelete='CASCADE')
    )
    # image sera apenas o nome caso queira salvar a imagem no banco de dados
    # mudar para BYTEA para salvar a imagem no banco de dados
    name: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, init=False, default=datetime.now
    )

    # Relacionamento com o ProductModel
    product: Mapped['ProductModel'] = relationship(  # noqa
        'ProductModel', init=False, back_populates='images'
    )  # noqa


@event.listens_for(ImageModel, 'before_insert')
def update_created_at(mapper, connection, target: ImageModel):
    target.created_at = datetime.now()
