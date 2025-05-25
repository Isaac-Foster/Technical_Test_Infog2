from src.infra.models.client import ClientModel

from src.adapter.repository.public import BaseRepo
from src.interfaces.schema.client import (
    ClientRegisterSchema,
    ClientPublicSchema,
)


class ClientRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.model = ClientModel
        self.public = ClientPublicSchema

    def create(self, data: ClientRegisterSchema):
        already = self.find_all(email=data.email, document=data.document)
        if already.get('results'):
            return Exception('Client already exists')

        model = self.model(**data.dict())

        with self.session() as session:
            session.add(model)
            session.commit()
            session.refresh(model)

        return self.public(**model.__dict__)
