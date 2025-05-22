from src.infra.database.sql import reg, engine

from src.infra.models import user #noqa

def init_sql():
    reg.metadata.create_all(engine)