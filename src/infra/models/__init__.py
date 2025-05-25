from src.infra.database.sql import reg, engine

from src.infra.models import (
    user,  # noqa
    client,  # noqa
    product,  # noqa
    image,  # noqa
    order,  # noqa
    order_item,  # noqa
)


def init_sql():
    reg.metadata.create_all(engine)
