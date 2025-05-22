from sqlalchemy import String, Integer, Enum, ARRAY
from sqlalchemy.orm import mapped_column, Mapped

from src.infra.database.sql import reg
from src.infra.enums.user import RoleEnum


@reg.mapped_as_dataclass
class UserModel:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(60))
    document: Mapped[str] = mapped_column(String(11), unique=True, index=True)
    roles: Mapped[list[RoleEnum]] = mapped_column(
        ARRAY(Enum(RoleEnum, name='roles', create_constraint=True)),
        init=False,
        default=lambda: [RoleEnum.CLIENT],
    )
