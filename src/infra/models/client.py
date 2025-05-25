from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from src.infra.database.sql import reg


@reg.mapped_as_dataclass
class ClientModel:
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    # password: Mapped[str] = mapped_column(String(60))
    document: Mapped[str] = mapped_column(String(11), unique=True, index=True)
